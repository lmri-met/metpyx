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
import json

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
            self.json_data = json_data
            self.calibration_coefficients = json_data[identification]['calibration coefficient']
            self.calibration_coefficients_correction = json_data[identification]['correction factor']
            self.electrometer_range_correction = json_data[identification]['electrometer range']
        else:
            self.json_data = None
            self.calibration_coefficients = None
            self.calibration_coefficients_correction = None
            self.electrometer_range_correction = None

    def measure_current(self, time_readings, charge_readings, time_unit, charge_unit, background=False,
                        background_current=None, temperature_readings=None, pressure_readings=None, current_unit=None,
                        temperature_unit=None, pressure_unit=None):

        # Check units compliance wit units convention
        d.check_units_compliance(time=time_unit, charge=charge_unit, temperature=temperature_unit,
                                 pressure=pressure_unit, current=current_unit, air_kerma=None)

        # If ionization chamber is open, get environmental reference conditions and temperatures in kelvin
        if self.open_chamber:
            reference_pressure = d.REFERENCE_PRESSURE
            reference_temperature_k = d.celsius_to_kelvin(d.REFERENCE_TEMPERATURE)
            temperature_readings_k = d.celsius_to_kelvin(temperature_readings)
        else:
            reference_pressure = None
            reference_temperature_k = None
            temperature_readings_k = None

        # Compute current
        current_readings = d.get_current(time=time_readings, charge=charge_readings, background=background,
                                         background_current=background_current, open_detector=self.open_chamber,
                                         temperature=temperature_readings_k, pressure=pressure_readings,
                                         reference_temperature=reference_temperature_k,
                                         reference_pressure=reference_pressure)

        # Store results in IonizationChamberMeasurement object
        measurement = IonizationChamberMeasurement(
            ionization_chamber=self, time_readings=time_readings, charge_readings=charge_readings,
            current_readings=current_readings, temperature_readings=temperature_readings,
            pressure_readings=pressure_readings)

        return measurement

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

            # Update ionization chamber measurement
            current_measurement.set_air_kerma_rate(air_kerma_rate_readings)

            return current_measurement
        else:
            raise NotCalibratedError(magnitude='air kerma rate')

    def measure_operational_magnitude(self, kerma_measurement, radiation_quality_csv, measurement_magnitude,
                                      radiation_quality, electrometer_range):
        if self.calibrated:
            # Get kerma rate from ionization chamber measurement
            mean_air_kerma_rate = abs(kerma_measurement.air_kerma_rate.value)

            # Read radiation quality data file
            csv_data = pd.read_csv(radiation_quality_csv, header=1)
            # Get kerma-to-measurement magnitude conversion factor from CSV
            conversion_coefficient = \
            csv_data.loc[csv_data['Quality'] == radiation_quality, f'h_k[{measurement_magnitude}]'].values[0]

            # Get electrometer range correction factor from ionization chamber
            electrometer_range_correction = self.electrometer_range_correction[electrometer_range]

            # Get air attenuation factor from CSV data
            air_attenuation_coefficient = csv_data.loc[csv_data['Quality'] == radiation_quality, 'mu_air'].values[0]
            # Define air width
            air_width = 0.001293
            # Get pressure from ionization chamber measurement
            mean_pressure = kerma_measurement.pressure.value
            # Get temperature from ionization chamber measurement in celsius
            mean_temperature = kerma_measurement.temperature.value
            # Get temperature from ionization chamber measurement in kelvin
            mean_temperature_k = d.celsius_to_kelvin(kerma_measurement.temperature.value)
            # Change reference temperature units to kelvin
            reference_temperature_k = d.celsius_to_kelvin(d.REFERENCE_TEMPERATURE)
            # Compute air density correction factor
            air_density_correction = d.get_attenuation_factor(
                attenuation_coefficient=air_attenuation_coefficient, width=air_width, temperature=mean_temperature_k,
                pressure=mean_pressure, reference_temperature=reference_temperature_k,
                reference_pressure=d.REFERENCE_PRESSURE)

            # Compute operational magnitude rate (per second)
            ctv_rate = d.get_operational_magnitude_rate(
                kerma_rate=mean_air_kerma_rate, conversion_coefficient=conversion_coefficient,
                electrometer_range_correction=electrometer_range_correction,
                air_density_correction=air_density_correction)
            # Compute operational magnitude rate (per hour)
            ctv_rate = d.second_to_hour(ctv_rate)

            # Compute integration time
            integration_time = sum(kerma_measurement.time_readings)
            # Compute integral operational magnitude
            ctv_integral = d.get_integral_magnitude(magnitude_rate=ctv_rate,
                                                    integration_time=d.second_to_hour(integration_time))

            results = (
                f'Mean kerma rate: {mean_air_kerma_rate}\n\n'
                f'Measurement magnitude: {measurement_magnitude}\n'
                f'Data file: {radiation_quality_csv}\n'
                f'Conversion coefficient: {conversion_coefficient}\n\n'
                f'Electrometer range: {electrometer_range}\n'
                f'Electrometer range correction: {electrometer_range_correction}\n\n'
                f'Air attenuation coefficient correction: {air_attenuation_coefficient}\n'
                f'Air width: {air_width}\n'
                f'Mean pressure: {mean_pressure}\n'
                f'Mean temperature: {mean_temperature}\n'
                f'Air density correction: {air_density_correction}\n\n'
                f'CTV of the operational magnitude rate: {ctv_rate}\n'
                f'Integration time: {integration_time}\n'
                f'CTV of the integral operational magnitude: {ctv_integral}\n'
            )
            return results
        else:
            raise NotCalibratedError(magnitude='operational magnitude')


class IonizationChamberMeasurement:
    def __init__(self, ionization_chamber, time_readings, charge_readings,
                 current_readings, temperature_readings=None, pressure_readings=None):
        # Basic measurement is current with no environmental correction nor background current
        self.ionization_chamber_id = ionization_chamber.identification
        self.ionization_chamber_json = ionization_chamber.json_data
        self.time_readings = list(time_readings)
        self.charge_readings = list(charge_readings)
        self.current_readings = list(current_readings)
        self.time = m.series_to_magnitude(time_readings, d.UNITS_CONVENTION['Time'])
        self.charge = m.series_to_magnitude(charge_readings, d.UNITS_CONVENTION['Charge'])
        self.current = m.series_to_magnitude(current_readings, d.UNITS_CONVENTION['Current'])
        if ionization_chamber.open_chamber:
            self.reference_temperature = d.REFERENCE_TEMPERATURE
            self.reference_pressure = d.REFERENCE_PRESSURE
            self.temperature_readings = list(temperature_readings)
            self.pressure_readings = list(pressure_readings)
            self.temperature = m.series_to_magnitude(temperature_readings, d.UNITS_CONVENTION['Temperature'])
            self.pressure = m.series_to_magnitude(pressure_readings, d.UNITS_CONVENTION['Pressure'])
        # if magnitude == 'air kerma rate' or magnitude == 'operational magnitude':
        #     self.radiation_quality = radiation_quality
        #     self.calibration_coefficient = ionization_chamber_json[ionization_chamber_id]['calibration coefficient'][
        #         get_radiation_quality_series(radiation_quality)]
        #     self.calibration_coefficient_correction = \
        #         ionization_chamber_json[ionization_chamber_id]['correction factor'][radiation_quality]
        #     self.distance_factor = distance_factor
        #     self.radiation_quality_csv = radiation_quality_csv
        #     self.air_kerma_rate_readings = air_kerma_rate_readings
        #     self.air_kerma_rate = m.series_to_magnitude(air_kerma_rate_readings, d.UNITS_CONVENTION['Air kerma'])
        # if magnitude == 'operational magnitude':
        #     self.operational_magnitude = operational_magnitude
        #     self.conversion_coefficient = radiation_quality_csv.loc[
        #         radiation_quality_csv['Quality'] == radiation_quality, f'h_k[{operational_magnitude}]'].values[0]
        #     self.electrometer_range = electrometer_range
        #     self.electrometer_range_correction = ionization_chamber_json[ionization_chamber_id]['electrometer range'][
        #         electrometer_range]
        #     self.air_attenuation_coefficient = \
        #         radiation_quality_csv.loc[radiation_quality_csv['Quality'] == radiation_quality, 'mu_air'].values[0]
        #     self.air_width = air_width
        #     self.air_density_correction = air_density_correction
        #     self.operational_magnitude_rate = operational_magnitude_rate
        #     self.integration_time = integration_time
        #     self.integral_operational_magnitude = integral_operational_magnitude
        # else:
        #     raise Exception(
        #         "Available measurement magnitudes are: current, air kerma rate and operational magnitude")

    def to_json(self):
        json.dumps(self.__dict__)

    # def set_current_attributes(self):
    #     pass
    #
    # def set_kerma_attributes(self):
    #     pass
    #
    # def set_operational_magnitude_attributes(self):
    #     pass

    def __repr__(self):
        return f'{self.to_json()}'

    # def set_air_kerma_rate(self, air_kerma_rate_readings):
    #     self.air_kerma_rate_readings = air_kerma_rate_readings
    #     self.air_kerma_rate = m.series_to_magnitude(self.air_kerma_rate_readings, d.UNITS_CONVENTION['Air kerma'])

    # def to_dataframe(self):
    #     # Get readings, magnitudes, names and units
    #     readings = [self.time_readings, self.charge_readings, self.temperature_readings, self.pressure_readings,
    #                 self.current_readings, self.air_kerma_rate_readings]
    #     magnitudes = [self.time, self.charge, self.temperature, self.pressure, self.current, self.air_kerma_rate]
    #     names = ['Time', 'Charge', 'Temperature', 'Pressure', 'Current', 'Air kerma']
    #     units = [d.UNITS_CONVENTION[name] for name in names if name in d.UNITS_CONVENTION.keys()]
    #
    #     # Build dictionary for dataframe building
    #     measurement_dict = {}
    #     for name, unit, readings, magnitude in zip(names, units, readings, magnitudes):
    #         if readings is not None:
    #             key = f'{name} ({unit})'
    #             value = [*readings, magnitude.value, magnitude.uncertainty, magnitude.percentage_uncertainty()]
    #             measurement_dict[key] = value
    #
    #     # Build dataframe
    #     df = pd.DataFrame(measurement_dict)
    #
    #     # Define and insert first column of the dataframe and set it as index
    #     first_column = [f'Reading {i + 1}' for i in range(len(df) - 3)] + ['Mean', 'Uncertainty', '% Uncertainty']
    #     df.insert(loc=0, column='#', value=np.array(first_column))
    #     df.set_index(keys='#', inplace=True)
    #
    #     return df


class IonizationChamberException(Exception):
    # Base class for IonizationChamber class exceptions
    pass


class NotCalibratedError(IonizationChamberException):
    # Not calibrated ionization chamber: cannot compute air kerma rate or operational magnitudes
    def __init__(self, magnitude):
        self.msg = 'The ionization chamber is not calibrated.'
        self.magnitude = magnitude

    def __str__(self):
        return f'{self.msg} Cannot compute {self.magnitude}.'
