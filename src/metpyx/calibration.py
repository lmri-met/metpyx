"""
Module to calibrate an x-ray measuring device.

Available x-ray qualities:
    L-series: L-10, L-20, L-30, L-35, L-55, L-70, L-100, L-125, L-170, L-210, L-240
    N-series: N-10, N-15, N-20, N-25, N-30, N-40, N-60, N-80, N-100, N-120, N-150, N-200, N-250, N-300
    W-series: W-30, W-40, W-60, W-80, W-110, W-150, W-200, W-250, W-300

Available calibration magnitudes:
    Magnitude Symbol Unit
    Exposicion X R
    Kerma en aire K_air Gy
    Absorbed dose en aire D_air Gy
    Dose equivalent H Sv
    Ambient dose equivalent H* Sv
    Directional dose equivalent H' Sv
    Personal dose equivalent H_p Sv

"""
import json
from math import sqrt

import numpy as np
import pandas as pd


class Magnitude:
    """
    Class to perform simple operations with magnitudes including units and uncertainties.

    It allows to define magnitudes with value, uncertainty and unit.
    It allows to compute simple operations providing the result for the magnitude value, uncertainty and unit.
    Available operations include summation, subtraction, multiplication and division.

    Magnitudes must have value, uncertainty and unit.
    Uncertainty can be provided in the same units of the magnitude or as a relative uncertainty.
    Magnitudes with zero value cannot be defined.
    Magnitudes without uncertainties can be defined with zero uncertainty.
    Non-dimensional magnitudes can be defined with an empty string unit.

    Magnitudes can be summed or subtracted as long as they have the same units.
    Magnitudes can be multiplied or divided independently of their units.
    The unit of the product or division is the concatenation of the units of the individual magnitude.

    Attributes
    ----------
    value : int or float
        Value of the magnitude.
    uncertainty : int or float
        Uncertainty of the magnitude in the units of the magnitude.
    unit : str
        Unit of the magnitude.


    Raises
    ------
    ValueError
        If uncertainty is negative.
    """

    def __init__(self, value, uncertainty, unit, relative_uncertainty=False):
        """
        Parameters
        ----------
        value : int or float
            Value of the magnitude.
        uncertainty : int or float
            Uncertainty of the magnitude.
        unit : str
            Unit of the magnitude.
        relative_uncertainty : bool, optional
            Type of uncertainty: False if absolute uncertainty, True if relative uncertainty (default False)
        """
        if uncertainty < 0:
            raise ValueError('Uncertainty must be positive.')
        self.value = value
        self.unit = unit
        if relative_uncertainty:
            self.uncertainty = uncertainty * abs(value)
        else:
            self.uncertainty = uncertainty

    def relative_uncertainty(self):
        """Return the relative uncertainty of the magnitude."""
        return self.uncertainty / abs(self.value)

    def percentage_uncertainty(self):
        """Return the percentage uncertainty of the magnitude."""
        return self.relative_uncertainty() * 100

    def __repr__(self):
        value = float(self.value)
        uncertainty = float(self.uncertainty)
        percentage_uncertainty = float(self.percentage_uncertainty())
        return f'{value} \u00B1 {uncertainty} {self.unit} ({percentage_uncertainty}%)'

    def __add__(self, other):
        """Magnitudes can be summed as long as they have the same units."""
        if self.unit == other.unit:
            value = self.value + other.value
            uncertainty = sqrt(self.uncertainty ** 2 + other.uncertainty ** 2)
            magnitude = Magnitude(value=value, uncertainty=uncertainty, unit=self.unit)
            return magnitude
        else:
            raise TypeError('Added magnitudes must have the same units.')

    def __sub__(self, other):
        """Magnitudes can be subtracted as long as they have the same units."""
        if self.unit == other.unit:
            value = self.value - other.value
            uncertainty = sqrt(self.uncertainty ** 2 + other.uncertainty ** 2)
            magnitude = Magnitude(value=value, uncertainty=uncertainty, unit=self.unit)
            return magnitude
        else:
            raise TypeError('Subtracted magnitudes must have the same units.')

    def __mul__(self, other):
        """The unit resulting from the product will be the concatenation of the individual magnitude units."""
        value = self.value * other.value
        unit = f'({self.unit}·{other.unit})'
        relative_uncertainty = sqrt(self.relative_uncertainty() ** 2 + other.relative_uncertainty() ** 2)
        magnitude = Magnitude(value=value, uncertainty=relative_uncertainty, unit=unit, relative_uncertainty=True)
        return magnitude

    def __truediv__(self, other):
        """The unit resulting from the division will be the concatenation of the individual magnitude units."""
        value = self.value / other.value
        unit = f'({self.unit}/{other.unit})'
        relative_uncertainty = sqrt(self.relative_uncertainty() ** 2 + other.relative_uncertainty() ** 2)
        magnitude = Magnitude(value=value, uncertainty=relative_uncertainty, unit=unit, relative_uncertainty=True)
        return magnitude


class IonizationChamber:
    REFERENCE_TEMPERATURE = 293.15  # K
    REFERENCE_PRESSURE = 101.325  # kPa
    CELSIUS_TO_KELVIN = 273.15

    def __init__(self, identification):
        self.identification = identification

    def measure_current_series(self, charge_readings, time_readings):
        # Units must be time in s and charge in C
        return list(np.array(charge_readings) / np.array(time_readings))

    def measure_ambient_corrected_current_series(self, charge_readings, time_readings, leak_current_value,
                                                 temperature_readings, pressure_readings):
        # Units must be: time in s, charge in C, pressure in kPa, temperature in C
        total_current = np.array(charge_readings) / np.array(time_readings)
        ambient_correction = (self.REFERENCE_PRESSURE / self.REFERENCE_TEMPERATURE) * (
                self.CELSIUS_TO_KELVIN + np.array(temperature_readings)) / np.array(pressure_readings)
        return list((total_current - leak_current_value) * ambient_correction)

    @staticmethod
    def series_to_magnitude(series, unit):
        mean = np.mean(series)
        mean_std = np.std(series) / np.sqrt(len(series))
        return Magnitude(value=mean, uncertainty=mean_std, unit=unit, relative_uncertainty=False)

    def measure_charge(self, charge_readings):
        return self.series_to_magnitude(series=charge_readings, unit='C')

    def measure_temperature(self, temperature_readings):
        return self.series_to_magnitude(series=temperature_readings, unit='ºC')

    def measure_pressure(self, pressure_readings):
        return self.series_to_magnitude(series=pressure_readings, unit='kPa')

    def measure_current(self, charge_readings, time_readings):
        current = self.measure_current_series(charge_readings=charge_readings, time_readings=time_readings)
        return self.series_to_magnitude(series=current, unit='A')

    def measure_ambient_corrected_current(self, charge_readings, time_readings, leak_current_value,
                                          temperature_readings, pressure_readings):
        current = self.measure_ambient_corrected_current_series(charge_readings=charge_readings,
                                                                time_readings=time_readings,
                                                                leak_current_value=leak_current_value,
                                                                temperature_readings=temperature_readings,
                                                                pressure_readings=pressure_readings)
        return self.series_to_magnitude(series=current, unit='A')

    @staticmethod
    def magnitudes_to_dataframe(magnitudes, names):
        values, uncertainties, units, relative_uncertainties = [], [], [], []
        for magnitude in magnitudes:
            values.append(magnitude.value)
            uncertainties.append(magnitude.uncertainty)
            units.append(magnitude.unit)
            relative_uncertainties.append(magnitude.relative_uncertainty())
        df = pd.DataFrame({'Magnitude': names, 'Value': values, 'Uncertainty': uncertainties, 'Units': units,
                           'Relative Uncertainty': relative_uncertainties})
        return df

    def detail_current_measurement(self, leak_charge_readings, leak_time_readings, charge_readings, time_readings,
                                   temperature_readings, pressure_readings):
        # Compute magnitudes and series
        leak_charge_magnitude = self.measure_charge(charge_readings=leak_charge_readings)
        leak_current_series = self.measure_current_series(time_readings=leak_time_readings,
                                                          charge_readings=leak_charge_readings)
        leak_current_magnitude = self.measure_current(time_readings=leak_time_readings,
                                                      charge_readings=leak_charge_readings)
        charge_magnitude = self.measure_charge(charge_readings=charge_readings)
        temperature_magnitude = self.measure_temperature(temperature_readings=temperature_readings)
        pressure_magnitude = self.measure_pressure(pressure_readings=pressure_readings)
        current_series = self.measure_ambient_corrected_current_series(charge_readings=charge_readings,
                                                                       time_readings=time_readings,
                                                                       leak_current_value=leak_current_magnitude.value,
                                                                       temperature_readings=temperature_readings,
                                                                       pressure_readings=pressure_readings)
        current_magnitude = self.measure_ambient_corrected_current(charge_readings=charge_readings,
                                                                   time_readings=time_readings,
                                                                   leak_current_value=leak_current_magnitude.value,
                                                                   temperature_readings=temperature_readings,
                                                                   pressure_readings=pressure_readings)
        # Compute series

        # Dataframe of series
        series_df = pd.DataFrame(
            {'Leak time (s)': leak_time_readings, 'Leak charge (C)': leak_charge_readings,
             'Leak current (A)': leak_current_series,
             'Time (s)': time_readings, 'Pressure (kPA)': pressure_readings, 'Temperature (ºC)': temperature_readings,
             'Charge (C)': charge_readings,
             'Current (A)': current_series})
        # Dataframe of magnitudes

        magnitudes = [leak_charge_magnitude, leak_current_magnitude, pressure_magnitude, temperature_magnitude,
                      charge_magnitude, current_magnitude]
        names = ['Leak charge', 'Leak current', 'Pressure', 'Temperature', 'Charge', 'Current']
        magnitudes_df = self.magnitudes_to_dataframe(magnitudes=magnitudes, names=names)
        return series_df, magnitudes_df


# TODO: rename series arguments to _readings
class StandardIonizationChamber(IonizationChamber):
    def __init__(self, identification, calibration_coefficients, correction_factors):
        super().__init__(identification=identification)
        self.calibration_coefficients = calibration_coefficients
        self.correction_factors = correction_factors

    @staticmethod
    def get_radiation_quality_series(radiation_quality):
        series = radiation_quality.split('-')[0]
        return f'{series}-series'

    def measure_air_kerma_series(self, current, radiation_quality):
        # Units must be: time in s, charge in C, pressure in kPa, temperature in C
        # Get calibration coefficient and correction factor
        radiation_quality_series = self.get_radiation_quality_series(radiation_quality)
        calibration_coefficient = self.calibration_coefficients[radiation_quality_series]
        correction_factor = self.correction_factors[radiation_quality]
        # Get distance factor
        distance_factor = 0.206378548  # TODO: compute distance factor
        # Compute air kerma
        air_kerma_series = np.array(current) * calibration_coefficient * correction_factor * distance_factor
        return list(air_kerma_series)

    def measure_air_kerma(self, current, radiation_quality):
        air_kerma = self.measure_air_kerma_series(current=current, radiation_quality=radiation_quality)
        return self.series_to_magnitude(series=air_kerma, unit='Gy/s')


class Calibration:
    UNITS = {
        'H´(0.07)': {'rate': 'Sv/h', 'integral': 'Sv'},
        'H´(3)': {'rate': 'Sv/h', 'integral': 'Sv'},
        'H*(10)': {'rate': 'Sv/h', 'integral': 'Sv'},
        'X': {'rate': 'R/h', 'integral': 'R'},
        'K_air': {'rate': 'Gy/h', 'integral': 'Gy'},
        'D_air': {'rate': 'Gy/h', 'integral': 'Gy'},
    }

    def __init__(self, radiation_quality_series, radiation_quality, measurement_magnitude, standard_chamber):
        self.radiation_quality_series = radiation_quality_series
        self.radiation_quality = radiation_quality
        self.measurement_magnitude = measurement_magnitude
        self.standard_chamber = standard_chamber

    def read_conversion_coefficient(self, conversion_coefficients_csv):
        df = pd.read_csv(conversion_coefficients_csv, header=1)
        df.set_index(df.columns[0], inplace=True)
        conversion_coefficient = df.loc[self.radiation_quality, self.measurement_magnitude]
        return conversion_coefficient

    def read_measurement_magnitude_units(self):
        return self.UNITS[self.measurement_magnitude]

    def read_standard_chamber_calibration_factor(self, standard_chambers_csv):
        with open(standard_chambers_csv, 'r') as file:
            data = json.load(file)
        standard_chamber_calibration_factor = data[self.standard_chamber]['calibration factor'][
            f'{self.radiation_quality_series}-series']
        return standard_chamber_calibration_factor

    def read_standard_chamber_corrector_factor(self, standard_chambers_csv):
        with open(standard_chambers_csv, 'r') as file:
            data = json.load(file)
        standard_chamber_corrector_factor = data[self.standard_chamber]['correction factor'][self.radiation_quality]
        return standard_chamber_corrector_factor
