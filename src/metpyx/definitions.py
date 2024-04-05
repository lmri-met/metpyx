from math import exp

REFERENCE_TEMPERATURE = 20  # 293.15 K, 20ºC
REFERENCE_PRESSURE = 101.325  # 101.325 kPa, 1 atm
UNITS_CONVENTION = {'Time': 's', 'Pressure': 'kPa', 'Temperature': 'ºC', 'Charge': 'C', 'Current': 'A',
                    'Air kerma': 'Gy/s'}


def celsius_to_kelvin(celsius):
    # T(K) = T(ºC) + 273.15
    return celsius + 273.15


def kelvin_to_celsius(kelvin):
    # T(K) = T(ºC) + 273.15
    return 273.15 - kelvin


def hour_to_second(hours):
    # 1 h = 3600 s
    return hours * 3600


def second_to_hour(seconds):
    # 1 h = 3600 s
    return seconds / 3600


def check_units_compliance(time=None, charge=None, temperature=None, pressure=None, current=None, air_kerma=None):
    keys = ['Time', 'Charge', 'Temperature', 'Pressure', 'Current', 'Air kerma']
    values = [time, charge, temperature, pressure, current, air_kerma]
    units_dictionary = dict(zip(keys, values))
    for key in units_dictionary:
        if units_dictionary[key] is not None and units_dictionary[key] != UNITS_CONVENTION[key]:
            message = f'Unit of {key} must be {UNITS_CONVENTION[key]}, provided unit is {units_dictionary[key]}'
            raise ValueError(message)


def get_environmental_correction(temperature, pressure, reference_temperature, reference_pressure):
    """
    Calculate the environmental correction factor.

    Parameters
    ----------
    temperature : float
        Temperature in Kelvin (K).
    pressure : float
        Pressure in pascals (Pa).
    reference_temperature : float
        Reference temperature in Kelvin (K).
    reference_pressure : float
        Reference pressure in pascals (Pa).

    Returns
    -------
    float
        The environmental correction factor, which is non-dimensional.

    Notes
    -----
    The environmental correction factor is calculated using the formula:

    .. math:: \frac{{\text{{reference\_pressure}}}}{{\text{{reference\_temperature}}}} \times \frac{{\text{{temperature}}}}{{\text{{pressure}}}}

    where `reference_pressure` and `reference_temperature` are reference values used for calibration.

    Examples
    --------
    >>> get_environmental_correction(300, 101325, 298.15, 101325)
    1.0000494031588694
    """
    return (reference_pressure / reference_temperature) * (temperature / pressure)


def get_current(time, charge, background=None, open_detector=False, temperature=None, pressure=None,
                reference_temperature=None, reference_pressure=None):
    """
    Calculate the current.

    Parameters
    ----------
    time : float
        Time in seconds (s).
    charge : float
        Charge in coulombs (C).
    background : float, optional
        Background current in amperes (A). Default is None.
    open_detector : bool, optional
        Flag indicating whether the detector is open. Default is False.
    temperature : float, optional
        Temperature in Kelvin (K). Default is None.
    pressure : float, optional
        Pressure in pascals (Pa). Default is None.
    reference_temperature : float, optional
        Reference temperature in Kelvin (K). Default is None.
    reference_pressure : float, optional
        Reference pressure in pascals (Pa). Default is None.

    Returns
    -------
    float
        The calculated current in amperes (A).

    Notes
    -----
    The current is calculated by dividing the charge by the time. If `background` is provided,
    it is subtracted from the current. If `open_detector` is True, the current is multiplied
    by the environmental correction factor obtained using the `get_environmental_correction`
    function.

    Examples
    --------
    >>> get_current(10, 5)
    0.5
    >>> get_current(10, 5, background=0.1)
    0.4
    >>> get_current(10, 5, open_detector=True, temperature=300, pressure=101325, reference_temperature=298.15, reference_pressure=101325)
    1.0000494031588694
    """
    current = charge / time
    if background:
        current = current - background
    if open_detector:
        correction = get_environmental_correction(temperature, pressure, reference_temperature, reference_pressure)
        current = current * correction
    return current


def get_kerma_rate(current, calibration_coefficient, calibration_coefficients_correction, distance_factor):
    """
    Calculate the kerma rate.

    Parameters
    ----------
    current : float
        Current in amperes (A).
    calibration_coefficient : float
        Calibration coefficient in gray per ampere (Gy/A).
    calibration_coefficients_correction : float
        Calibration coefficient correction, non-dimensional.
    distance_factor : float
        Distance factor, non-dimensional.

    Returns
    -------
    float
        The kerma rate in gray per second (Gy/s).

    Notes
    -----
    The kerma rate is calculated using the formula:

    .. math:: \text{{current}} \times \text{{calibration_coefficient}} \times \text{{calibration_coefficients_correction}} \times \text{{distance_factor}}

    where `current` is the current in amperes, `calibration_coefficient` is the calibration coefficient in Gy/A,
    `calibration_coefficients_correction` is the correction factor for calibration coefficients, and
    `distance_factor` is the distance factor.

    Examples
    --------
    >>> get_kerma_rate(0.5, 0.1, 1.2, 2.0)
    0.12
    """
    return current * calibration_coefficient * calibration_coefficients_correction * distance_factor


def get_operational_magnitude_rate(kerma_rate, conversion_coefficient, electrometer_range_correction,
                                   air_density_correction):
    """
    Calculate the operational magnitude rate.

    Parameters
    ----------
    kerma_rate : float
        Kerma rate in gray per second (Gy/s).
    conversion_coefficient : float
        Conversion coefficient in the unit of the operational magnitude per gray.
    electrometer_range_correction : float
        Electrometer range correction, non-dimensional.
    air_density_correction : float
        Air density correction, non-dimensional.

    Returns
    -------
    float
        The operational magnitude rate in the unit of the operational magnitude per second.

    Notes
    -----
    The operational magnitude rate is calculated using the formula:

    .. math:: \text{{kerma_rate}} \times \text{{conversion_coefficient}} \times \text{{electrometer_range_correction}} \times \text{{air_density_correction}}

    where `kerma_rate` is the kerma rate in Gy/s, `conversion_coefficient` is the conversion coefficient in the unit
    of the operational magnitude per gray, `electrometer_range_correction` is the correction factor for electrometer
    range, and `air_density_correction` is the correction factor for air density.

    Examples
    --------
    >>> get_operational_magnitude_rate(0.5, 0.1, 1.2, 2.0)
    0.12
    """
    return kerma_rate * conversion_coefficient * electrometer_range_correction * air_density_correction


def get_integral_magnitude(magnitude_rate, integration_time):
    """
    Calculate the integral magnitude.

    Parameters
    ----------
    magnitude_rate : float
        Magnitude rate in the unit of the magnitude per second.
    integration_time : float
        Integration time in seconds (s).

    Returns
    -------
    float
        The integral magnitude.

    Notes
    -----
    The integral magnitude is calculated by multiplying the magnitude rate by the integration time.

    .. math:: \text{{integral_magnitude}} = \text{{magnitude_rate}} \times \text{{integration_time}}

    where `magnitude_rate` is the rate of change of magnitude in the unit of the magnitude per second,
    and `integration_time` is the duration over which the magnitude rate is integrated.

    Examples
    --------
    >>> get_integral_magnitude(0.5, 10)
    5.0
    """
    return magnitude_rate * integration_time


def get_attenuation_factor(attenuation_coefficient, width, temperature, pressure, reference_temperature, reference_pressure):
    correction = get_environmental_correction(temperature, pressure, reference_temperature, reference_pressure)
    return exp(attenuation_coefficient * width * correction)
