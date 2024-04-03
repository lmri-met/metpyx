"""
Calibration steps:
1. Select and read initial information:
- Select measurement magnitude
- Select radiation quality
- Read kerma-to-operational magnitude conversion coefficient (magnitude, quality).
- Read unit of integral and rate measurement magnitude
- Select reference chamber (initially there will only be one, the 557, but there may be two)
- Select quality series
- Read chamber calibration factor for quality series
- Read correction factor of calibration factor for quality

2. Simultaneous measurements of the reference chamber and the monitoring chamber

2.1. Leakage current measurements (shutter closed):
- Select irradiation time for leakage measurements
- Measure the electrometer charge
- Calculate leakage current

2.2. Kerma measurement (shutter open):
- Select irradiation time for leakage measurements
- Measure the electrometer charge
- Measure pressure (1 barometer)
- Measure temperature (2 probes connected to the same thermometer)
- Calculate current intensity (excluding leakages and corrected for reference pressure and temperature conditions)
- Calculate kerma rate (includes distance factor)

3. VCV of the operational magnitude rate
- Kerma rate (calculated previously)
- Kerma-to-measurement magnitude conversion factor (previously chosen)
- Electrometer range correction factor (from the reference chamber calibration certificate, RANGE LOW HIGH table,
  select range)
- Air density correction factor (read from Hp tab, air attenuation table)

4. Equipment measurements
- Equipment background measurements (shutter closed)
- Equipment readings
- Measure pressure (only if chamber is open to air)
- Measure temperature (only if chamber is open to air)
- Correct for pressure and temperature if chamber is open
- Correct for equipment background

5. Calculate dose rate calibration factor
- VCV of previously calculated magnitude between equipment reading
- The monitoring chamber is used to verify beam stability
- Monitoring chamber measurements should be the same when measuring with the reference chamber and when measuring with
  the equipment because you have the same voltage and current conditions
- VCV * monitoring chamber measurement when measuring with the equipment
- Equipment reading * monitoring chamber measurement when measuring with the reference chamber
- These products are sieverts/hour * current intensity
- The calibration factor is the relationship between both

6. Distance factor
Simultaneous measurements of the reference chamber and the monitoring chamber at two distances

6.1. Leakage current measurements (shutter closed):
- Select irradiation time for leakage measurements
- Measure the electrometer charge
- Calculate leakage current

6.2. Current intensity measurement (shutter open):
- Select irradiation time for leakage measurements
- Measure the electrometer charge
- Measure pressure (1 barometer)
- Measure temperature (2 probes connected to the same thermometer)
- Calculate current intensity (excluding leakages and corrected to reference pressure and temperature conditions)

6.3. Calculate distance correction factor

Note: All measurements: 5 measurements in 60 seconds
"""
import json

import numpy as np
import pandas as pd

from src.metpyx.ionization_chamber import IonizationChamber, get_radiation_quality_series

# ----------------------------------------------------------------------------------------------------------------------

# 1. Select and read initial information
# --------------------------------------

# 1.1. Select initial information
# -------------------------------
# - Select measurement magnitude
# - Select radiation quality
# - Select quality series
# - Select reference chamber (initially there will only be one, the 557, but there may be two)

# 1.2. Read initial information
# -----------------------------
# - Read kerma-to-operational magnitude conversion coefficient (magnitude, quality).
# - Read unit of integral and rate measurement magnitude
# - Read chamber calibration factor for quality series
# - Read correction factor of calibration factor for quality

# User provided information
measurement_magnitude = 'H*(10)'
radiation_quality = 'L-170'
conversion_coefficients = './assets/radiation_quality_data.csv'
reference_chamber_id = 'ns557'
reference_chamber_data = './assets/standard_chambers.json'
electrometer_range = 'low'
monitor_chamber_id = 'monitor'
detector = None
output_file = './output.txt'

# Read radiation quality data file
csv_data = pd.read_csv(conversion_coefficients, header=1)
# Read reference ionization chamber data file
with open(reference_chamber_data, 'r') as file:
    json_data = json.load(file)
# Define reference ionization chamber
reference = IonizationChamber(identification=reference_chamber_id, calibrated=True, open_chamber=True, json_data=json_data)

# Reference radiation information
radiation_quality_series = get_radiation_quality_series(radiation_quality)
air_width = 0.001293
air_attenuation_coefficient = csv_data.loc[csv_data['Quality'] == 'L-170', 'mu_air'].values[0]
conversion_coefficient = csv_data.loc[csv_data['Quality'] == 'L-170', f'h_k[{measurement_magnitude}]'].values[0]
# Reference chamber information
calibration_coefficient = json_data[reference_chamber_id]["calibration coefficient"][radiation_quality_series]
correction_factor = json_data[reference_chamber_id]["correction factor"][radiation_quality]
electrometer_range_correction = json_data[reference_chamber_id]["electrometer range"][electrometer_range]
# Environmental conditions information
reference_temperature = reference.REFERENCE_TEMPERATURE
reference_pressure = reference.REFERENCE_PRESSURE
# Other information
celsius_to_kelvin = reference.CELSIUS_TO_KELVIN
hour_to_second = reference.HOUR_TO_SECOND

# Results
section1 = (
    f'IR-14D: Calibration of radiation measuring devices\n'
    f'\n'
    f'1. INITIAL INFORMATION\n'
    f'\n'
    f'1.1. Reference radiation:\n'
    f'Radiation quality series: {radiation_quality_series}\n'
    f'Radiation quality: {radiation_quality}\n'
    f'Air attenuation coefficient: {air_attenuation_coefficient}\n'
    f'Conversion coefficient: {conversion_coefficient}'
    f'Data file: {conversion_coefficients}\n'
    f'\n'
    f'2.1. Reference chamber:\n'
    f'Identification: {reference_chamber_id}\n'
    f'Calibration coefficient: {calibration_coefficient}\n'
    f'Correction factor: {correction_factor}\n'
    f'Electrometer range: {electrometer_range}\n'
    f'Electrometer range correction: {electrometer_range_correction}\n'
    f'Data file: {reference_chamber_data}\n'
    f'\n'
    f'1.4. Environmental conditions:\n'
    f'Reference temperature: {reference_temperature}\n'
    f'Reference pressure: {reference_pressure}\n'
    f'\n'
    f'1.3. Other information\n'
    f'Measurement magnitude: {measurement_magnitude}\n'
    f'Monitor chamber ID: {monitor_chamber_id}\n'
    f'Detector ID: {detector}\n'
    f'Distance factor: {0.206378548} (WARNING! Hardcoded value)\n'  # TODO: Hardcoded value
    f'Celsius to Kelvin conversion: {celsius_to_kelvin}\n'
    f'Hour to seconds conversion: {hour_to_second}\n'
    f'\n'
)

# ----------------------------------------------------------------------------------------------------------------------

# Summary

# 2. Simultaneous measurements of the reference chamber and the monitoring chamber
# 2.1. Measurements of the monitoring chamber
# 2.1.1. Leakage current measurements (shutter closed)
# - Select irradiation time
# - Measure the electrometer charge
# - Calculate leakage current
# 2.1.2. Current measurement (shutter open)
# - Select irradiation time
# - Measure the electrometer charge
# - Calculate current
# 2.2. Measurements of the reference chamber
# 2.2.1. Leakage current measurements (shutter closed)
# - Select irradiation time
# - Measure the electrometer charge
# - Calculate leakage current
# 2.2.2. Current measurement (shutter open)
# - Select irradiation time
# - Measure the electrometer charge
# - Calculate current
# 2.2.3. Kerma measurement (shutter open)
# - Measure pressure
# - Measure temperature
# - Calculate distance factor
# - Calculate air kerma rate
# 2.3. VCV of the operational magnitude rate
# - Kerma rate (calculated previously)
# - Kerma-to-measurement magnitude conversion factor (previously chosen)
# - Electrometer range correction factor (from reference chamber calibration certificate, RANGE LOW HIGH table)
# - Air density correction factor (read from Hp tab, air attenuation table)

# Implementation

# 2. Simultaneous measurements of the reference chamber and the monitoring chamber
# --------------------------------------------------------------------------------

# 2.1. Measurements of the monitoring chamber
# -------------------------------------------
# - Define monitor ionization chamber
monitor = IonizationChamber(identification=monitor_chamber_id, calibrated=False, open_chamber=True)
# - Time and charge readings for leakage current measurement (shutter closed)
monitor_leakage_time_readings = [60, 60, 60, 60]
monitor_leakage_charge_readings = [-8.50E-13, -4.30E-13, -2.70E-13, -7.50E-13]
# - Time, charge, pressure and temperature readings for current measurement (shutter open)
monitor_time_readings = [60, 60, 60, 60, 60]
monitor_pressure_readings = [93.642, 93.642, 93.638, 93.638, 93.633]
monitor_temperature_readings = [20.63, 20.6, 20.6, 20.6, 20.63]
monitor_charge_readings = [4.16E-12, 3.54E-12, 4.18E-12, 4.38E-12, 4.36E-12]
# - Measure leakage current and current
monitor_measurement = monitor.measure(
    magnitude='current',
    leakage_time_readings=monitor_leakage_time_readings, leakage_charge_readings=monitor_leakage_charge_readings,
    time_readings=monitor_time_readings, charge_readings=monitor_charge_readings,
    pressure_readings=monitor_pressure_readings, temperature_readings=monitor_temperature_readings,
    radiation_quality=None)

# 2.2. Measurements of the reference chamber
# ------------------------------------------
# - Time and charge readings for leakage current measurement (shutter closed)
reference_leakage_time_readings = [60, 60, 60, 60]
reference_leakage_charge_readings = [-1.00E-14, -1.10E-13, -1.00E-13, 3.00E-14]
# - Time, charge, pressure and temperature readings for current measurement (shutter open)
reference_time_readings = [60, 60, 60, 60, 60]
reference_pressure_readings = [93.642, 93.642, 93.638, 93.638, 93.633]
reference_temperature_readings = [20.88, 20.91, 20.9, 20.94, 20.96]
reference_charge_readings = [-1.162E-11, -1.168E-11, -1.169E-11, -1.175E-11, -1.164E-11]
# - Calculate distance factor TODO: Calculate, now hardcoded value)
# - Measure leakage current, current and air kerma
reference_measurement = reference.measure(
    magnitude='air_kerma',
    leakage_time_readings=reference_leakage_time_readings, leakage_charge_readings=reference_leakage_charge_readings,
    time_readings=reference_time_readings, charge_readings=reference_charge_readings,
    pressure_readings=reference_pressure_readings, temperature_readings=reference_temperature_readings,
    radiation_quality=radiation_quality)

# TODO: Small discrepancy in air kerma uncertainty, compare what excel and python functions do to compute the std.
# TODO: Why compute 5 intensities and air kerma readings and not compute it from the mean charge? Uncertainties?

# 2.3. CTV of the operational magnitude rate
# ------------------------------------------
# - Kerma rate (calculated previously)
# - Kerma-to-measurement magnitude conversion factor (previously chosen)
# - Electrometer range correction factor (from reference chamber calibration certificate, RANGE LOW HIGH table)
# - Air density correction factor (read from Hp tab, air attenuation table)

mean_pressure = reference_measurement.loc['Mean', 'Pressure (kPa)']
mean_temperature = reference_measurement.loc['Mean', 'Temperature (ºC)'] + celsius_to_kelvin
air_density_correction = np.exp(
    air_attenuation_coefficient * air_width * (mean_pressure / reference_pressure) * (reference_temperature / mean_temperature))
# TODO: When calculating ambient correction in reference chamber intensity readings, reference temperature is 293.15 K
#  (20ºC) and reference pressure is 101.325 kPa (1 atm). However, when calculating air density correction, reference
#  temperature is 273.15 K and reference pressure is 101.25 kPa. The air density correction is 1.00017 in the first case
#  and 1.00016 in the second case. I am going to use the first reference values, but this differs from the spreed sheet.
#  Also, I though that the reference laboratory conditions were 25ºC and 1 atm, we are using 20ºC.

mean_air_kerma_rate = abs(reference_measurement.loc['Mean', 'Air kerma (Gy/s)'])
ctv_rate = mean_air_kerma_rate * conversion_coefficient * electrometer_range_correction * air_density_correction * hour_to_second
integration_time = sum(reference_time_readings) / hour_to_second
ctv_integral = ctv_rate * integration_time

# Results
# -------
section2 = (
    f'2. SIMULTANEOUS MEASUREMENTS OF REFERENCE CHAMBER AND MONITOR CHAMBER\n'
    f'\n'
    f'2.1.Measurements of the monitor chamber\n'
    f'{monitor_measurement.to_string(index=True)}\n'
    f'\n'
    f'2.2. Measurements of the reference chamber\n'
    f'{reference_measurement.to_string(index=True)}\n'
    f'\n'
    f'2.3. CTV of the operational magnitude rate\n'
    f'Mean air kerma rate: {mean_air_kerma_rate}\n'
    f'Conversion coefficient: {conversion_coefficient}\n'
    f'Electrometer range correction: {electrometer_range_correction}\n'
    f'Air density correction: {air_density_correction}\n'
    f'CTV of the operational magnitude rate: {ctv_rate}\n'
    f'Integration time: {integration_time}\n'
    f'CTV of the integral operational magnitude: {ctv_integral}\n'
    f'\n'
)

# ----------------------------------------------------------------------------------------------------------------------

# 3. Simultaneous measurements of the detector and the monitoring chamber
# - Equipment background measurements (shutter closed)
# - Equipment readings
# - Measure pressure (only if chamber is open to air)
# - Measure temperature (only if chamber is open to air)
# - Correct for pressure and temperature if chamber is open
# - Correct for equipment background

# ----------------------------------------------------------------------------------------------------------------------

# 4. Calculate dose rate calibration factor
# - VCV of previously calculated magnitude between equipment reading
# - The monitoring chamber is used to verify beam stability
# - Monitoring chamber measurements should be the same when measuring with the reference chamber and when measuring
#   with the equipment because you have the same voltage and current conditions
# - VCV * monitoring chamber measurement when measuring with the equipment
# - Equipment reading * monitoring chamber measurement when measuring with the reference chamber
# - These products are sieverts/hour * current intensity
# - The calibration factor is the relationship between both

# ----------------------------------------------------------------------------------------------------------------------

# 5. Distance factor
# Simultaneous measurements of the reference chamber and the monitoring chamber at two distances
# 5.1. Leakage current measurements (shutter closed):
# - Select irradiation time for leakage measurements
# - Measure the electrometer charge
# - Calculate leakage current
# 5.2. Current intensity measurement (shutter open):
# - Select irradiation time for leakage measurements
# - Measure the electrometer charge
# - Measure pressure (1 barometer)
# - Measure temperature (2 probes connected to the same thermometer)
# - Calculate current intensity (excluding leakages and corrected to reference pressure and temperature conditions)
# 5.3. Calculate distance correction factor

# ----------------------------------------------------------------------------------------------------------------------

# 6. Write results to a text file
with open(output_file, 'w') as f:
    f.write(section1 + section2)
print(f'Calibration results written to {output_file}')

# ----------------------------------------------------------------------------------------------------------------------

# CLASS: CALIBRATION

# radiation_quality_series = 'L'
# radiation_quality = 'L-170'
# measurement_magnitude = 'H*(10)'
# standard_chamber = 'ns557'
# conversion_coefficients_csv = 'assets/conversion_coefficients.csv'
#
# c = cal.Calibration(
#     radiation_quality_series=radiation_quality_series,
#     radiation_quality=radiation_quality,
#     measurement_magnitude=measurement_magnitude,
#     standard_chamber=standard_chamber,
# )
#
# print('Attributes:')
# rqs = c.radiation_quality_series
# rq = c.radiation_quality
# mm = c.measurement_magnitude
# sc = c.standard_chamber
#
# print('Methods:')
# cc = c.read_conversion_coefficient(conversion_coefficients_csv=conversion_coefficients_csv)
# mmu = c.read_measurement_magnitude_units()
# sccalf = c.read_standard_chamber_calibration_factor('assets/standard_chambers.json')
# sccorf = c.read_standard_chamber_corrector_factor('assets/standard_chambers.json')
