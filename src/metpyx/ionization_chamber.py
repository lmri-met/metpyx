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
import numpy as np
import pandas as pd

import src.metpyx.definitions as d
import src.metpyx.magnitude as m


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
        d.check_units_compliance(time=time_unit, charge=charge_unit)
        current_readings = d.get_current(time=time_readings, charge=charge_readings)
        return IonizationChamberMeasurement(ionization_chamber_id=self.identification, time_readings=time_readings,
                                            charge_readings=charge_readings, current_readings=current_readings)

    def measure_current(self, time_readings, charge_readings, time_unit, charge_unit, background=None,
                        temperature_readings=None, pressure_readings=None, current_unit=None, temperature_unit=None,
                        pressure_unit=None):
        d.check_units_compliance(time=time_unit, charge=charge_unit, temperature=temperature_unit,
                                 pressure=pressure_unit,
                                 current=current_unit, air_kerma=None)
        if self.open_chamber:
            reference_pressure = d.REFERENCE_PRESSURE
            reference_temperature = d.celsius_to_kelvin(d.REFERENCE_TEMPERATURE)
            temperature_readings = d.celsius_to_kelvin(temperature_readings)
        else:
            reference_pressure = None
            reference_temperature = None

        current_readings = d.get_current(time=time_readings, charge=charge_readings, background=background,
                                         open_detector=self.open_chamber,
                                         temperature=temperature_readings, pressure=pressure_readings,
                                         reference_temperature=reference_temperature,
                                         reference_pressure=reference_pressure)
        return IonizationChamberMeasurement(ionization_chamber_id=self.identification, time_readings=time_readings,
                                            charge_readings=charge_readings, current_readings=current_readings)

    def measure_air_kerma_rate(self, current_measurement, radiation_quality):
        if self.calibrated:
            # Get current readings
            current_readings = current_measurement.current_readings
            # Get ionization chamber calibration coefficient and correction factor
            radiation_quality_series = get_radiation_quality_series(radiation_quality)
            calibration_coefficient = self.calibration_coefficients[radiation_quality_series]
            calibration_coefficients_correction = self.calibration_coefficients_correction[radiation_quality]
            # Get distance factor
            distance_factor = 0.206378548  # TODO: compute distance factor
            # Compute air kerma readings
            air_kerma_rate_readings = d.get_kerma_rate(
                current=current_readings, calibration_coefficient=calibration_coefficient,
                calibration_coefficients_correction=calibration_coefficients_correction,
                distance_factor=distance_factor)
            current_measurement.set_air_kerma_rate(air_kerma_rate_readings)
            return current_measurement
        else:
            raise Exception("Cannot compute air kerma: the ionization chamber is not calibrated.")

    def measure_operational_magnitude(self):
        pass


class IonizationChamberMeasurement:
    def __init__(self, ionization_chamber_id, time_readings, charge_readings, current_readings,
                 temperature_readings=None, pressure_readings=None, air_kerma_rate_readings=None):
        self.ionization_chamber_id = ionization_chamber_id
        self.time_readings = time_readings
        self.charge_readings = charge_readings
        self.temperature_readings = temperature_readings
        self.pressure_readings = pressure_readings
        self.current_readings = current_readings
        self.air_kerma_rate_readings = air_kerma_rate_readings
        self.time = m.series_to_magnitude(self.time_readings, d.UNITS_CONVENTION['Time'])
        self.charge = m.series_to_magnitude(self.charge_readings, d.UNITS_CONVENTION['Charge'])
        self.current = m.series_to_magnitude(self.current_readings, d.UNITS_CONVENTION['Current'])
        if temperature_readings:
            self.temperature = m.series_to_magnitude(self.temperature_readings, d.UNITS_CONVENTION['Temperature'])
        else:
            self.temperature = None
        if pressure_readings:
            self.pressure = m.series_to_magnitude(self.pressure_readings, d.UNITS_CONVENTION['Pressure'])
        else:
            self.pressure = None
        if air_kerma_rate_readings:
            self.air_kerma_rate = m.series_to_magnitude(self.air_kerma_rate_readings, d.UNITS_CONVENTION['Air kerma'])
        else:
            self.air_kerma_rate = None

    def set_air_kerma_rate(self, air_kerma_rate_readings):
        self.air_kerma_rate_readings = air_kerma_rate_readings
        self.air_kerma_rate = m.series_to_magnitude(self.air_kerma_rate_readings, d.UNITS_CONVENTION['Air kerma'])

    def to_dataframe(self):
        # Get readings, magnitudes, names and units
        readings = [self.time_readings, self.charge_readings, self.temperature_readings, self.pressure_readings,
                    self.current_readings, self.air_kerma_rate_readings]
        magnitudes = [self.time, self.charge, self.temperature, self.pressure, self.current, self.air_kerma_rate]
        names = ['Time', 'Charge', 'Temperature', 'Pressure', 'Current', 'Air kerma']
        units = [d.UNITS_CONVENTION[name] for name in names if name in d.UNITS_CONVENTION.keys()]

        # Build dictionary for dataframe building
        measurement_dict = {}
        for name, unit, readings, magnitude in zip(names, units, readings, magnitudes):
            if readings is not None:
                key = f'{name} ({unit})'
                value = [*readings, magnitude.value, magnitude.uncertainty, magnitude.percentage_uncertainty()]
                measurement_dict[key] = value

        # Build dataframe
        df = pd.DataFrame(measurement_dict)

        # Define and insert first column of the dataframe and set it as index
        first_column = [f'Reading {i + 1}' for i in range(len(df) - 3)] + ['Mean', 'Uncertainty', '% Uncertainty']
        df.insert(loc=0, column='#', value=np.array(first_column))
        df.set_index(keys='#', inplace=True)

        return df
