"""
Module to calibrate an x-ray measuring device.

Available x-ray qualities:
    L-series: L-10, L-20, L-30, L-35, L-55, L-70, L-100, L-125, L-170, L-210, L-240
    N-series: N-10, N-15, N-20, N-25, N-30, N-40, N-60, N-80, N-100, N-120, N-150, N-200, N-250, N-300
    W-series: W-30, W-40, W-60, W-80, W-110, W-150, W-200, W-250, W-300

Available calibration magnitudes:
    Magnitude Symbol Unit
    Exposition X R
    Air kerma K_air Gy
    Air absorbed dose D_air Gy
    Dose equivalent H Sv
    Ambient dose equivalent H* Sv
    Directional dose equivalent H' Sv
    Personal dose equivalent H_p Sv

"""
import json

import pandas as pd


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
