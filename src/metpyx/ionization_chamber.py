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
import src.metpyx.magnitude as m
import src.metpyx.magnitude_definitions as md

REFERENCE_TEMPERATURE = 20  # 293.15 K, 20ºC
REFERENCE_PRESSURE = 101.325  # 101.325 kPa, 1 atm
UNITS_CONVENTION = {'Time': 's', 'Pressure': 'kPa', 'Temperature': 'ºC', 'Charge': 'C', 'Current': 'A',
                    'Air kerma': 'Gy/s'}


def celsius_to_kelvin(celsius):
    # T(K) = T(ºC) + 273.15
    return celsius + 273.15


def hour_to_second(hours):
    # 1 h = 3600 s
    return hours * 3600


def check_units_compliance(time=None, charge=None, temperature=None, pressure=None, current=None, air_kerma=None):
    keys = ['Time', 'Charge', 'Temperature', 'Pressure', 'Current', 'Air kerma']
    values = [time, charge, temperature, pressure, current, air_kerma]
    units_dictionary = dict(zip(keys, values))
    for key in units_dictionary:
        if units_dictionary[key] is not None and units_dictionary[key] != UNITS_CONVENTION[key]:
            message = f'Unit of {key} must be {UNITS_CONVENTION[key]}, provided unit is {units_dictionary[key]}'
            raise ValueError(message)


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

    def measure_leakage_current(self, time_readings, charge_readings, time_unit, charge_unit):
        check_units_compliance(time=time_unit, charge=charge_unit)
        current_readings = md.get_current(time=time_readings, charge=charge_readings)
        return IonizationChamberMeasurement(ionization_chamber_id=self.identification, time_readings=time_readings,
                                            charge_readings=charge_readings, current_readings=current_readings)

    def measure_current(self, time_readings, charge_readings, background=None, temperature_readings=None,
                        pressure_readings=None):
        if self.open_chamber:
            reference_pressure = REFERENCE_PRESSURE
            reference_temperature = celsius_to_kelvin(REFERENCE_TEMPERATURE)
            temperature_readings = celsius_to_kelvin(temperature_readings)
        else:
            reference_pressure = None
            reference_temperature = None

        current_readings = md.get_current(time=time_readings, charge=charge_readings, background=background,
                                          open_detector=self.open_chamber,
                                          temperature=temperature_readings, pressure=pressure_readings,
                                          reference_temperature=reference_temperature,
                                          reference_pressure=reference_pressure)
        return IonizationChamberMeasurement(ionization_chamber_id=self.identification, time_readings=time_readings,
                                            charge_readings=charge_readings, current_readings=current_readings)

    def measure_air_kerma_rate(self, current, radiation_quality):
        if self.calibrated:
            # Get ionization chamber calibration coefficient and correction factor
            radiation_quality_series = get_radiation_quality_series(radiation_quality)
            calibration_coefficient = self.calibration_coefficients[radiation_quality_series]
            calibration_coefficients_correction = self.calibration_coefficients_correction[radiation_quality]
            # Get distance factor
            distance_factor = 0.206378548  # TODO: compute distance factor
            # Compute air kerma readings
            air_kerma_rate = md.get_kerma_rate(current, calibration_coefficient, calibration_coefficients_correction,
                                               distance_factor)
            return air_kerma_rate
        else:
            raise Exception("Cannot compute air kerma: the ionization chamber is not calibrated.")

    def get_ctv_operational_magnitude(self):
        pass


class IonizationChamberMeasurement:
    def __init__(self, ionization_chamber_id, time_readings, charge_readings, current_readings,
                 temperature_readings=None, pressure_readings=None, air_kerma_readings=None):
        self.ionization_chamber_id = ionization_chamber_id
        self.time_readings = time_readings
        self.charge_readings = charge_readings
        self.temperature_readings = temperature_readings
        self.pressure_readings = pressure_readings
        self.current_readings = current_readings
        self.air_kerma_readings = air_kerma_readings
        self.time = m.series_to_magnitude(self.time_readings, UNITS_CONVENTION['Time'])
        self.charge = m.series_to_magnitude(self.charge_readings, UNITS_CONVENTION['Charge'])
        self.current = m.series_to_magnitude(self.current_readings, UNITS_CONVENTION['Current'])
        if temperature_readings:
            self.temperature = m.series_to_magnitude(self.temperature_readings, UNITS_CONVENTION['Temperature'])
        else:
            self.temperature = None
        if pressure_readings:
            self.pressure = m.series_to_magnitude(self.pressure_readings, UNITS_CONVENTION['Pressure'])
        else:
            self.pressure = None
        if air_kerma_readings:
            self.air_kerma = m.series_to_magnitude(self.air_kerma_readings, UNITS_CONVENTION['Air kerma'])
        else:
            self.air_kerma = None
