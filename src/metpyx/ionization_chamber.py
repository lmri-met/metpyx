import numpy as np
import pandas as pd

from src.metpyx.magnitude import series_to_magnitude, magnitudes_to_dataframe


def get_radiation_quality_series(radiation_quality):
    series = radiation_quality.split('-')[0]
    return f'{series}-series'


def results_dataframe(names, readings, magnitudes):

    measurement_dict = {}
    for name, readings, magnitude in zip(names, readings, magnitudes):
        key = f'{name} ({magnitude.unit})'
        value = [*readings, magnitude.value, magnitude.uncertainty, magnitude.percentage_uncertainty()]
        measurement_dict[key] = value

    df = pd.DataFrame(measurement_dict)

    first_column = [f'Reading {i + 1}' for i in range(len(df) - 3)] + ['Mean', 'Uncertainty', '% Uncertainty']
    df.insert(0, '#', first_column)
    df.set_index('#', inplace=True)

    return df


class IonizationChamber:
    REFERENCE_TEMPERATURE = 293.15  # K
    REFERENCE_PRESSURE = 101.325  # kPa
    CELSIUS_TO_KELVIN = 273.15

    def __init__(self, identification, calibrated, open_chamber, calibration_coefficients=None,
                 correction_factors=None):
        self.identification = identification
        self.calibrated = calibrated
        self.open_chamber = open_chamber
        self.calibration_coefficients = calibration_coefficients
        self.correction_factors = correction_factors

    def get_ambient_correction(self, temperature_readings, pressure_readings):
        # Units must be: pressure in kPa, temperature in C
        ambient_correction = (self.REFERENCE_PRESSURE / self.REFERENCE_TEMPERATURE) * (
                self.CELSIUS_TO_KELVIN + np.array(temperature_readings)) / np.array(pressure_readings)
        return ambient_correction

    def measure_current_readings(self, charge_readings, time_readings, open_shutter, leak_current_value=None,
                                 temperature_readings=None, pressure_readings=None):
        # Units must be: time in s, charge in C, pressure in kPa, temperature in C, current in A
        # If the shutter is closed, leakage current is measured (total current is measured, no leakage current is
        # subtracted and no ambient correction is applied):
        current = np.array(charge_readings) / np.array(time_readings)
        # If the shutter is open and the ionization chamber is closed, total current is measured and leakage current
        # must be subtracted (no ambient correction is applied)
        if open_shutter:
            current = current - leak_current_value
            # If the shutter is open and the ionization chamber is open, total current is measured, leakage current must
            # be subtracted and ambient correction must be applied:
            if self.open_chamber:
                ambient_correction = self.get_ambient_correction(temperature_readings, pressure_readings)
                current = current * ambient_correction
        return current

    def measure_air_kerma_readings(self, current_readings, radiation_quality):
        # Units must be: time in s, charge in C, pressure in kPa, temperature in C
        if self.calibrated:
            # Get ionization chamber calibration coefficient and correction factor
            radiation_quality_series = get_radiation_quality_series(radiation_quality)
            calibration_coefficient = self.calibration_coefficients[radiation_quality_series]
            correction_factor = self.correction_factors[radiation_quality]
            # Get distance factor
            distance_factor = 0.206378548  # TODO: compute distance factor
            # Compute air kerma readings
            air_kerma_readings = np.array(
                current_readings) * calibration_coefficient * correction_factor * distance_factor
            return list(air_kerma_readings)
        else:
            raise Exception("Cannot compute air kerma: the ionization chamber is not calibrated.")

    def measure_leakage(self, time_readings, charge_readings):
        # Leakage current measurements (closed shutter)
        current_readings = self.measure_current_readings(time_readings=time_readings, charge_readings=charge_readings, open_shutter=False)

        # Get mean of magnitudes
        time = series_to_magnitude(series=time_readings, unit='s')
        charge = series_to_magnitude(series=charge_readings, unit='C')
        current = series_to_magnitude(series=current_readings, unit='A')

        # Define lists to build dataframe
        names = ['Leakage time', 'Leakage charge', 'Leakage current']
        units = ['s', 'C' 'A']
        readings = [time_readings, charge_readings, current_readings]
        magnitudes = [time, charge, current]
        # magnitudes = [series_to_magnitude(series=reading, unit=unit) for (reading, unit) in zip(readings, units)]

        # Build dataframe
        leakage = results_dataframe(names, readings, magnitudes)

        return leakage

    def measure_current(self, time_readings, charge_readings, pressure_readings, temperature_readings, mean_leakage_current):
        # Current measurements (open shutter)
        current_readings = self.measure_current_readings(
            charge_readings=charge_readings, time_readings=time_readings, open_shutter=True,
            leak_current_value=mean_leakage_current, temperature_readings=temperature_readings,
            pressure_readings=pressure_readings)

        # Get mean of magnitudes
        time = series_to_magnitude(series=time_readings, unit='s')
        pressure = series_to_magnitude(series=pressure_readings, unit='kPa')
        temperature = series_to_magnitude(series=temperature_readings, unit='ºC')
        charge = series_to_magnitude(series=charge_readings, unit='C')
        current = series_to_magnitude(series=current_readings, unit='A')

        # Define lists to build dataframe
        names = ['Time', 'Pressure', 'Temperature', 'Charge', 'Current']
        readings = [time_readings, pressure_readings, temperature_readings, charge_readings, current_readings]
        magnitudes = [time, pressure, temperature, charge, current]

        # Build dataframe
        measurements_df = results_dataframe(names, readings, magnitudes)

        return measurements_df

    def measure_air_kerma(self, current_readings, radiation_quality):
        # Air kerma measurements (open shutter)
        air_kerma_readings = self.measure_air_kerma_readings(current_readings=current_readings,
                                                             radiation_quality=radiation_quality)
        # Get mean of magnitudes
        air_kerma = series_to_magnitude(series=air_kerma_readings, unit='Gy/s')

        # Define lists to build dataframe
        names = ['Air kerma']
        readings = [air_kerma_readings]
        magnitudes = [air_kerma]

        # Build dataframe
        measurements_df = results_dataframe(names, readings, magnitudes)

        return measurements_df

    def measure(self, leakage, current, air_kerma, leakage_time_readings=None, leakage_charge_readings=None,
                time_readings=None, charge_readings=None, pressure_readings=None, temperature_readings=None,
                radiation_quality=None):
        if leakage:
            # Leakage current measurements (closed shutter)
            leakage = self.measure_leakage(time_readings=leakage_time_readings, charge_readings=leakage_charge_readings)
            measurement = leakage
            if current:
                # Current measurements (open shutter)
                leakage_current_value = leakage.loc['Mean', 'Leakage current (A)']
                current = self.measure_current(
                    charge_readings=charge_readings, time_readings=time_readings, temperature_readings=temperature_readings,
                    pressure_readings=pressure_readings, mean_leakage_current=leakage_current_value)
                measurement = pd.merge(leakage, current, left_index=True, right_index=True, how='outer')
                custom_order = [f'Reading {i + 1}' for i in range(len(measurement) - 3)] + ['Mean', 'Uncertainty', '% Uncertainty']
                measurement = measurement.reindex(custom_order)
                if air_kerma:
                    # Air kerma measurements (open shutter)
                    current_readings = current['Current (A)']
                    current_readings = current_readings.iloc[:-3]
                    air_kerma = self.measure_air_kerma(current_readings=current_readings, radiation_quality=radiation_quality)
                    measurement = pd.merge(measurement, air_kerma, left_index=True, right_index=True, how='outer')
                    custom_order = [f'Reading {i + 1}' for i in range(len(measurement) - 3)] + ['Mean', 'Uncertainty', '% Uncertainty']
                    measurement = measurement.reindex(custom_order)
            return measurement
        else:
            msg = (f'Options\n'
                   f'Measure leakage current: leakage=True, current=False, air_kerma=False\n'
                   f'Measure current: leakage=True, current=True, air_kerma=False\n'
                   f'Measure air kerma: leakage=True, current=True, air_kerma=True\n')
            raise Exception(msg)
