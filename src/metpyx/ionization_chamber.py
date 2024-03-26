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

from src.metpyx.magnitude import series_to_magnitude


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

    REFERENCE_TEMPERATURE = 293.15  # K
    REFERENCE_PRESSURE = 101.325  # kPa
    CELSIUS_TO_KELVIN = 273.15
    UNITS_CONVENTION = {'Time': 's', 'Pressure': 'kPa', 'Temperature': 'ºC', 'Charge': 'C', 'Current': 'A',
                        'Air kerma': 'Gy/s'}

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

    def _get_ambient_correction(self, temperature_readings, pressure_readings):
        """
        Calculates the ambient correction factor based on temperature and pressure readings.

        Parameters
        ----------
        temperature_readings : list
            List of temperature readings.
        pressure_readings : list
            List of pressure readings.

        Returns
        -------
        numpy.ndarray
            Array containing the ambient correction factors.
        """
        ambient_correction = (self.REFERENCE_PRESSURE / self.REFERENCE_TEMPERATURE) * (
                self.CELSIUS_TO_KELVIN + np.array(temperature_readings)) / np.array(pressure_readings)
        return ambient_correction

    def _get_current_readings(self, time_readings, charge_readings, open_shutter, mean_leakage=None,
                              temperature_readings=None, pressure_readings=None):
        """
        Calculates current readings considering various factors such as time, charge, and ambient conditions.

        This method computes the current readings based on the provided time and charge readings. If the shutter is
        open, it subtracts the mean leakage current. If the ionization chamber is open, an ambient correction is applied
        based on temperature and pressure readings. The resulting current readings are returned.

        Parameters
        ----------
        time_readings : list
            List of time readings in seconds.
        charge_readings : list
            List of charge readings in coulombs.
        open_shutter : bool
            Flag indicating whether the shutter is open.
        mean_leakage : float, optional
            Mean leakage current value in amperes, by default None.
        temperature_readings : list, optional
            List of temperature readings in Celsius, by default None.
        pressure_readings : list, optional
            List of pressure readings in kilopascals, by default None.

        Returns
        -------
        numpy.ndarray
            Array containing the calculated current readings in amperes.
        """
        current = np.array(charge_readings) / np.array(time_readings)
        if open_shutter:
            current = current - mean_leakage
            if self.open_chamber:
                ambient_correction = self._get_ambient_correction(temperature_readings, pressure_readings)
                current = current * ambient_correction
        return current

    def _get_air_kerma_readings(self, current_readings, radiation_quality):
        """
        Computes air kerma readings based on current readings and radiation quality.

        This method calculates the air kerma readings based on the provided current readings and radiation quality.
        It utilizes the ionization chamber's calibration coefficients and correction factors, along with a distance
        factor, to compute the air kerma. If the ionization chamber is not calibrated, an exception is raised.

        Parameters
        ----------
        current_readings : array_like
            Array of current readings in amperes.
        radiation_quality : str
            Quality of radiation.

        Returns
        -------
        list
            List containing the computed air kerma readings.

        Raises
        ------
        Exception
            If the ionization chamber is not calibrated.
        """
        if self.calibrated:
            # Get ionization chamber calibration coefficient and correction factor
            radiation_quality_series = get_radiation_quality_series(radiation_quality)
            calibration_coefficient = self.calibration_coefficients[radiation_quality_series]
            calibration_coefficients_correction = self.calibration_coefficients_correction[radiation_quality]

            # Get distance factor
            distance_factor = 0.206378548  # TODO: compute distance factor

            # Compute air kerma readings
            air_kerma_readings = np.array(
                current_readings) * calibration_coefficient * calibration_coefficients_correction * distance_factor
            return list(air_kerma_readings)
        else:
            raise Exception("Cannot compute air kerma: the ionization chamber is not calibrated.")

    def _measure_leakage(self, time_readings, charge_readings):
        """
        Measures leakage current based on time and charge readings.

        This method calculates the leakage current by invoking the `_get_current_readings` method with the shutter
        closed, thus measuring the total current without subtracting any leakage current. It then constructs a dataframe
        containing time, charge, and leakage current readings.

        Parameters
        ----------
        time_readings : array_like
            Array of time readings in seconds.
        charge_readings : array_like
            Array of charge readings in coulombs.

        Returns
        -------
        pandas.DataFrame
            DataFrame containing the measured leakage current readings.

        Notes
        -----
        This method is typically used when the shutter of the ionization chamber is closed.
        """
        # Leakage current readings
        current_readings = self._get_current_readings(time_readings=time_readings, charge_readings=charge_readings,
                                                      open_shutter=False)

        # Define list of readings to build dataframe
        readings = [time_readings, charge_readings, current_readings]

        # Build dataframe
        measurement = self._get_measurement_dataframe(magnitude='leakage_current', readings=readings)
        return measurement

    def _measure_current(self, leakage_time_readings, leakage_charge_readings, time_readings, charge_readings,
                         pressure_readings, temperature_readings):
        """
        Measures current considering leakage and environmental factors.

        This method calculates the current readings by accounting for leakage current, pressure, and temperature
        readings. It first measures the leakage current using `_measure_leakage` method, then calculates the
        mean leakage current. Using this mean leakage current, along with the provided time, charge, pressure, and
        temperature readings, it computes the current readings. Finally, it constructs a dataframe containing
        the measured current readings.

        Parameters
        ----------
        leakage_time_readings : array_like
            Array of time readings for leakage current measurement in seconds.
        leakage_charge_readings : array_like
            Array of charge readings for leakage current measurement in coulombs.
        time_readings : array_like
            Array of time readings for current measurement in seconds.
        charge_readings : array_like
            Array of charge readings for current measurement in coulombs.
        pressure_readings : array_like
            Array of pressure readings in kilopascals.
        temperature_readings : array_like
            Array of temperature readings in Celsius.

        Returns
        -------
        pandas.DataFrame
            DataFrame containing the measured current readings.

        Notes
        -----
        This method is typically used when the shutter of the ionization chamber is open.
        """
        # Leakage current dataframe
        leakage = self._measure_leakage(time_readings=leakage_time_readings, charge_readings=leakage_charge_readings)

        # Leakage current mean value
        mean_leakage_current = leakage.loc['Mean', 'Leakage current (A)']

        # Current readings
        current_readings = self._get_current_readings(
            charge_readings=charge_readings, time_readings=time_readings, open_shutter=True,
            mean_leakage=mean_leakage_current, temperature_readings=temperature_readings,
            pressure_readings=pressure_readings)

        # Define list of readings to build dataframe
        readings = [time_readings, pressure_readings, temperature_readings, charge_readings, current_readings]

        # Build dataframe
        current = self._get_measurement_dataframe(magnitude='current', readings=readings)

        # Merge dataframes
        measurement = self._merge_measurement_dataframes(df1=leakage, df2=current)

        return measurement

    def _measure_air_kerma(self, leakage_time_readings, leakage_charge_readings, time_readings, charge_readings,
                           pressure_readings, temperature_readings, radiation_quality):
        """
        Measures air kerma considering leakage and environmental factors.

        This method calculates the air kerma readings by accounting for leakage current, pressure, and temperature
        readings. It first measures the current using `_measure_current` method, then extracts the current readings
        and calculates the air kerma based on these readings and the provided radiation quality. Finally, it constructs
        a dataframe containing the measured air kerma readings.

        Parameters
        ----------
        leakage_time_readings : array_like
            Array of time readings for leakage current measurement in seconds.
        leakage_charge_readings : array_like
            Array of charge readings for leakage current measurement in coulombs.
        time_readings : array_like
            Array of time readings for current measurement in seconds.
        charge_readings : array_like
            Array of charge readings for current measurement in coulombs.
        pressure_readings : array_like
            Array of pressure readings in kilopascals.
        temperature_readings : array_like
            Array of temperature readings in Celsius.
        radiation_quality : str
            Quality of radiation.

        Returns
        -------
        pandas.DataFrame
            DataFrame containing the measured air kerma readings.

        Notes
        -----
        This method is typically used when the shutter of the ionization chamber is open and air kerma measurements
        are required.
        """
        # Current dataframe
        current = self._measure_current(
            leakage_time_readings=leakage_time_readings, leakage_charge_readings=leakage_charge_readings,
            time_readings=time_readings, charge_readings=charge_readings, pressure_readings=pressure_readings,
            temperature_readings=temperature_readings)

        # Current readings
        current_readings = current['Current (A)']
        current_readings = current_readings.iloc[:-3]

        # Air kerma readings
        air_kerma_readings = self._get_air_kerma_readings(current_readings=current_readings,
                                                          radiation_quality=radiation_quality)

        # Define list of readings to build dataframe
        readings = [air_kerma_readings]

        # Build dataframe
        air_kerma = self._get_measurement_dataframe(magnitude='air_kerma', readings=readings)

        # Merge dataframes
        measurement = self._merge_measurement_dataframes(df1=current, df2=air_kerma)

        return measurement

    def measure(self, magnitude, leakage_time_readings, leakage_charge_readings, time_readings=None,
                charge_readings=None, pressure_readings=None, temperature_readings=None, radiation_quality=None):
        """
        Measure various magnitudes of interest using the ionization chamber.

        This method allows the measurement of different magnitudes such as leakage current, current, and air kerma
        using the ionization chamber. It determines the type of measurement based on the provided magnitude parameter
        and calls the corresponding private methods to perform the measurement.

        Parameters
        ----------
        magnitude : {'leakage_current', 'current', 'air_kerma'}
            Type of magnitude to measure.
        leakage_time_readings : array_like
            Array of time readings for leakage current measurement in seconds.
        leakage_charge_readings : array_like
            Array of charge readings for leakage current measurement in coulombs.
        time_readings : array_like, optional
            Array of time readings for current measurement in seconds.
        charge_readings : array_like, optional
            Array of charge readings for current measurement in coulombs.
        pressure_readings : array_like, optional
            Array of pressure readings in kilopascals.
        temperature_readings : array_like, optional
            Array of temperature readings in Celsius.
        radiation_quality : str, optional
            Quality of radiation.

        Returns
        -------
        pandas.DataFrame
            DataFrame containing the measured magnitudes.

        Raises
        ------
        Exception
            If the provided magnitude is not one of the supported magnitudes.

        Notes
        -----
        This method is a high-level interface for performing ionization chamber measurements. It abstracts the
        measurement process and facilitates the easy measurement of various magnitudes.
        """
        if magnitude == 'leakage_current':
            # Leakage current measurements (closed shutter)
            return self._measure_leakage(time_readings=leakage_time_readings,
                                         charge_readings=leakage_charge_readings)
        elif magnitude == 'current':
            # Current measurements (open shutter)
            return self._measure_current(leakage_time_readings=leakage_time_readings,
                                         leakage_charge_readings=leakage_charge_readings, time_readings=time_readings,
                                         charge_readings=charge_readings, pressure_readings=pressure_readings,
                                         temperature_readings=temperature_readings)
        elif magnitude == 'air_kerma':
            # Air kerma measurements (open shutter)
            return self._measure_air_kerma(leakage_time_readings=leakage_time_readings,
                                           leakage_charge_readings=leakage_charge_readings, time_readings=time_readings,
                                           charge_readings=charge_readings, pressure_readings=pressure_readings,
                                           temperature_readings=temperature_readings,
                                           radiation_quality=radiation_quality)
        else:
            raise Exception(f'Measurable magnitudes are: "leakage_current", "current" and "air_kerma".')

    def _get_measurement_dataframe(self, magnitude, readings):
        """
        Create a pandas DataFrame from measurement readings.

        This method constructs a pandas DataFrame from the readings of a specific magnitude.
        The DataFrame includes individual readings, mean value, uncertainty, and percentage uncertainty
        for each magnitude. The index of the DataFrame is labeled with the corresponding reading numbers.

        Parameters
        ----------
        magnitude : str
            The magnitude for which the DataFrame is constructed.
            Should be one of 'leakage_current', 'current', or 'air_kerma'.
        readings : list
            A list containing the readings for the specified magnitude. The list should be in the format:
            [reading1, reading2, ..., readingN], where each reading is a list or array of numerical values.

        Returns
        -------
        pandas.DataFrame
            DataFrame containing the measurements, mean value, uncertainty, and percentage uncertainty
            for the specified magnitude.

        Raises
        ------
        Exception
            If the magnitude provided is not one of 'leakage_current', 'current', or 'air_kerma'.

        Notes
        -----
        This method is used internally to organize measurement data into a structured DataFrame format
        for further analysis and visualization. It is typically called within the context of other methods
        within the IonizationChamber class.
        """
        # Define magnitudes names to include in the dataframe
        if magnitude == 'leakage_current':
            names = ['Time', 'Charge', 'Current']
        elif magnitude == 'current':
            names = ['Time', 'Pressure', 'Temperature', 'Charge', 'Current']
        elif magnitude == 'air_kerma':
            names = ['Air kerma']
        else:
            raise Exception(f'Measurable magnitudes are: "leakage_current", "current" and "air_kerma".')

        # Get units of the magnitudes
        units = [self.UNITS_CONVENTION[name] for name in names if name in self.UNITS_CONVENTION.keys()]

        # Rename leakage current magnitudes
        if magnitude == 'leakage_current':
            names = [f'Leakage {name.lower()}' for name in names]

        # Build magnitudes from readings
        magnitudes = [series_to_magnitude(series=reading, unit=unit) for (reading, unit) in zip(readings, units)]

        # Build dictionary for dataframe building
        measurement_dict = {}
        for name, readings, magnitude in zip(names, readings, magnitudes):
            key = f'{name} ({magnitude.unit})'
            value = [*readings, magnitude.value, magnitude.uncertainty, magnitude.percentage_uncertainty()]
            measurement_dict[key] = value

        # Build dataframe
        df = pd.DataFrame(measurement_dict)

        # Define first column of the dataframe
        first_column = [f'Reading {i + 1}' for i in range(len(df) - 3)] + ['Mean', 'Uncertainty', '% Uncertainty']

        # Insert first column
        df.insert(loc=0, column='#', value=np.array(first_column))

        # Set index to the first column
        df.set_index(keys='#', inplace=True)

        return df

    @staticmethod
    def _merge_measurement_dataframes(df1, df2):
        """
        Merge two pandas DataFrames representing measurement data.

        This method merges two DataFrames representing measurement data, typically for different magnitudes,
        into a single DataFrame. It then reorders the index of the merged DataFrame to follow a specific pattern
        for readability and consistency.

        Parameters
        ----------
        df1 : pandas.DataFrame
            The first DataFrame containing measurement data.
        df2 : pandas.DataFrame
            The second DataFrame containing measurement data.

        Returns
        -------
        pandas.DataFrame
            Merged DataFrame with the index reordered for consistency.

        Notes
        -----
        This method is particularly useful for combining measurement data from different sources or measurements
        of different magnitudes into a single coherent DataFrame for analysis and visualization.
        """
        df = pd.merge(df1, df2, left_index=True, right_index=True, how='outer')
        index_order = [f'Reading {i + 1}' for i in range(len(df) - 3)] + ['Mean', 'Uncertainty', '% Uncertainty']
        return df.reindex(index_order)
