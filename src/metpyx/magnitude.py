from math import sqrt

import numpy as np
import pandas as pd


def series_to_magnitude(series, unit):
    mean = np.mean(series)
    mean_std = np.std(series) / np.sqrt(len(series))
    return Magnitude(value=mean, uncertainty=mean_std, unit=unit, relative_uncertainty=False)


def magnitudes_to_dataframe(magnitudes, names):
    values, uncertainties, units, percentage_uncertainties = [], [], [], []
    for magnitude in magnitudes:
        values.append(magnitude.value)
        uncertainties.append(magnitude.uncertainty)
        units.append(magnitude.unit)
        percentage_uncertainties.append(magnitude.percentage_uncertainty())
    df = pd.DataFrame({'Magnitude': names, 'Value': values, 'Uncertainty': uncertainties, 'Units': units,
                       'Uncertainty (%)': percentage_uncertainties})
    return df


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
