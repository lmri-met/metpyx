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
- Electrometer range correction factor (from the reference chamber calibration certificate, RANGE LOW HIGH table, select range)
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
- Monitoring chamber measurements should be the same when measuring with the reference chamber and when measuring with the equipment because you have the same voltage and current conditions
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

import pandas as pd

from src.metpyx.ionization_chamber import IonizationChamber, get_radiation_quality_series

# 2. Simultaneous measurements of the reference chamber and the monitoring chamber

# Readings of the monitoring chamber

# Readings for leakage current measurements (shutter closed)
monitor_leakage_time_readings = [60, 60, 60, 60]
monitor_leakage_charge_readings = [-8.50E-13, -4.30E-13, -2.70E-13, -7.50E-13]
# Readings for current measurement (shutter open)
monitor_time_readings = [60, 60, 60, 60, 60]
monitor_pressure_readings = [93.642, 93.642, 93.638, 93.638, 93.633]
monitor_temperature_readings = [20.63, 20.6, 20.6, 20.6, 20.63]
monitor_charge_readings = [4.16E-12, 3.54E-12, 4.18E-12, 4.38E-12, 4.36E-12]

# Readings of the reference chamber

# Readings for leakage current measurements (shutter closed)
reference_leakage_time_readings = [60, 60, 60, 60]
reference_leakage_charge_readings = [-1.00E-14, -1.10E-13, -1.00E-13, 3.00E-14]

# Readings for kerma measurement (shutter open)
reference_time_readings = [60, 60, 60, 60, 60]
reference_pressure_readings = [93.642, 93.642, 93.638, 93.638, 93.633]
reference_temperature_readings = [20.88, 20.91, 20.9, 20.94, 20.96]
reference_charge_readings = [-1.162E-11, -1.168E-11, -1.169E-11, -1.175E-11, -1.164E-11]

# Calculations

# Measurements with the monitor chamber

# Define monitor ionization chamber
monitor = IonizationChamber(identification='monitor', calibrated=False, open_chamber=True)

# Measure leakage current and current
monitor_measurement = monitor.measure(
    leakage=True, current=True, air_kerma=False,
    leakage_time_readings=monitor_leakage_time_readings, leakage_charge_readings=monitor_leakage_charge_readings,
    time_readings=monitor_time_readings, charge_readings=monitor_charge_readings,
    pressure_readings=monitor_pressure_readings, temperature_readings=monitor_temperature_readings,
    radiation_quality=None)

# Measurements with the reference chamber

# Read reference ionization chamber calibration coefficients and correction factors
with open('assets/standard_chambers.json', 'r') as file:
    data = json.load(file)
calibration_coefficients = data['ns557']['calibration coefficient']
corrector_factors = data['ns557']['correction factor']

# Define reference ionization chamber
reference = IonizationChamber(identification='reference', calibrated=True, open_chamber=True,
                              calibration_coefficients=calibration_coefficients, correction_factors=corrector_factors)

# Measure leakage current and air kerma
radiation_quality = 'L-170'
reference_measurement = reference.measure(
    leakage=True, current=True, air_kerma=False,
    leakage_time_readings=reference_leakage_time_readings, leakage_charge_readings=reference_leakage_charge_readings,
    time_readings=reference_time_readings, charge_readings=reference_charge_readings,
    pressure_readings=reference_pressure_readings, temperature_readings=reference_temperature_readings,
    radiation_quality=radiation_quality)


# Write results to a text file
with open('./output.txt', 'w') as f:
    f.write(f'IR-14D: Calibration of radiation measuring devices\n')
    f.write(f'\n')
    f.write(f'Reference radiation data\n')
    f.write(f'\n')
    f.write(f'Radiation quality: {radiation_quality}\n')
    f.write(f'Calibration coefficient: {calibration_coefficients[get_radiation_quality_series(radiation_quality)]}\n')
    f.write(f'Correction factor: {corrector_factors[radiation_quality]}\n')
    f.write(f'Distance factor: {0.206378548} (WARNING! Hardcoded value)\n')
    f.write(f'\n')
    f.write(f'Simultaneous measurements of the reference chamber and the monitoring chamber\n')
    f.write(f'\n')
    f.write(f'Measurements of the reference chamber\n')
    f.write(f'{reference_measurement.to_string(index=True)}\n')
    f.write(f'\n')
    f.write(f'Measurements of the monitor chamber\n')
    f.write(f'{monitor_measurement.to_string(index=True)}\n')
    f.write(f'\n')

print("Variables written to 'output.txt'")

# TODO: small discrepancy in uncertainty, compare what excel and python functions to compute the standard deviation do)

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
