"""
Ionization Chamber Module

This module provides a class `IonizationChamber` for representing an ionization chamber used for measuring
radiation quantities. It also includes utility functions for handling radiation quality and constructing
measurement dataframes.

Functions
---------
get_radiation_quality_series(radiation_quality)
    Extracts the series from a radiation quality string.

Classes
-------
IonizationChamber
    Class representing an ionization chamber for measuring radiation quantities.

Notes
-----
This module is part of the `metpyx` package, designed to facilitate meteorological data analysis.
"""
import src.metpyx.magnitude_definitions as md

REFERENCE_TEMPERATURE = 20  # 293.15 K, 20ºC
REFERENCE_PRESSURE = 101.325  # 101.325 kPa, 1 atm
CELSIUS_TO_KELVIN = 273.15  # T(K) = T(ºC) + 273.15
HOUR_TO_SECOND = 3600  # 1 h = 3600 s
UNITS_CONVENTION = {'Time': 's', 'Pressure': 'kPa', 'Temperature': 'ºC', 'Charge': 'C', 'Current': 'A',
                    'Air kerma': 'Gy/s'}


def get_radiation_quality_series(radiation_quality):
    """
    Extracts the series from a radiation quality string.

    Parameters
    ----------
    radiation_quality : str
        A string representing the radiation quality, typically in the format
        'series-type'. For example, 'N-10', 'L-30', etc.

    Returns
    -------
    str
        The extracted series from the radiation quality string, appended with
        the suffix '-series'. For example, if the input is 'N-10', the
        returned value will be 'N-series'.

    Examples
    --------
    >>> get_radiation_quality_series('N-10')
    'N-series'
    >>> get_radiation_quality_series('L-30')
    'L-series'
    """
    series = radiation_quality.split('-')[0]
    return f'{series}-series'


class IonizationChamber:
    """
    Class representing an ionization chamber for measuring radiation quantities.

    Attributes
    ----------
    REFERENCE_TEMPERATURE : float
        Reference temperature in Kelvin.
    REFERENCE_PRESSURE : float
        Reference pressure in kPa.
    CELSIUS_TO_KELVIN : float
        Conversion factor from Celsius to Kelvin.
    UNITS_CONVENTION : dict
        Dictionary mapping measurement quantities to their respective units.

    Methods
    -------
    __init__(identification, calibrated, open_chamber, json_data=None)
        Initializes the IonizationChamber object.
    _get_ambient_correction(temperature_readings, pressure_readings)
        Calculates the ambient correction factor based on temperature and pressure readings.
    _get_current_readings(time_readings, charge_readings, open_shutter, mean_leakage=None,
                           temperature_readings=None, pressure_readings=None)
        Calculates current readings considering various factors such as time, charge, and ambient conditions.
    _get_air_kerma_readings(current_readings, radiation_quality)
        Computes air kerma readings based on current readings and radiation quality.
    _measure_leakage(time_readings, charge_readings)
        Measures leakage current readings.
    _measure_current(leakage_time_readings, leakage_charge_readings, time_readings, charge_readings,
                     pressure_readings, temperature_readings)
        Measures current readings.
    _measure_air_kerma(leakage_time_readings, leakage_charge_readings, time_readings, charge_readings,
                       pressure_readings, temperature_readings, radiation_quality)
        Measures air kerma readings.
    measure(magnitude, leakage_time_readings, leakage_charge_readings, time_readings=None, charge_readings=None,
            pressure_readings=None, temperature_readings=None, radiation_quality=None)
        Measures various quantities based on the given magnitude.
    _get_measurement_dataframe(magnitude, readings)
        Builds a DataFrame from measurement readings.
    _merge_measurement_dataframes(df1, df2)
        Merges two DataFrames representing measurement data.
    """

    def __init__(self, identification, calibrated, open_chamber, json_data=None):
        """
        Initializes the IonizationChamber object.

        Parameters
        ----------
        identification : str
            Identifier for the ionization chamber.
        calibrated : bool
            Flag indicating whether the ionization chamber is calibrated.
        open_chamber : bool
            Flag indicating whether the ionization chamber is open.
        json_data : dict, optional
            JSON data containing calibration information, by default None
        """
        self.identification = identification
        self.calibrated = calibrated
        self.open_chamber = open_chamber
        if calibrated:
            self.calibration_coefficients = json_data[identification]['calibration coefficient']
            self.calibration_coefficients_correction = json_data[identification]['correction factor']
            self.electrometer_range_correction = json_data[identification]['electrometer range']
        else:
            self.calibration_coefficients = None
            self.calibration_coefficients_correction = None
            self.electrometer_range_correction = None

    def measure_current(self, time, charge, background=None, open_detector=False, temperature=None, pressure=None,
                              reference_temperature=None, reference_pressure=None):
        current = md.get_current(time, charge)
        current = md.get_current(time, charge, background=None)
        current = md.get_current(time, charge, open_detector=True, temperature=None, pressure=None, reference_temperature=None, reference_pressure=None)
        current = md.get_current(time, charge, background=None, open_detector=False, temperature=None, pressure=None, reference_temperature=None, reference_pressure=None)
        if background:
            pass
        if open_detector:
            pass

        pass

    def measure_kerma(self):
        pass
