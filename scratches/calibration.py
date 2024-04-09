import json
import numpy as np
import pandas as pd
from src.metpyx.definitions import REFERENCE_TEMPERATURE, REFERENCE_PRESSURE, celsius_to_kelvin, hour_to_second
from src.metpyx.ionization_chamber import IonizationChamber, get_radiation_quality_series


# # IR-14D: Calibration of radiation measuring devices
# Calibration steps:
# 1. Select and read initial information:
# - Select measurement magnitude
# - Select radiation quality
# - Read kerma-to-operational magnitude conversion coefficient (magnitude, quality).
# - Read unit of integral and rate measurement magnitude
# - Select reference chamber (initially there will only be one, the 557, but there may be two)
# - Select quality series
# - Read chamber calibration factor for quality series
# - Read correction factor of calibration factor for quality
#
# 2. Simultaneous measurements of the reference chamber and the monitoring chamber
#
# 2.1. Leakage current measurements (shutter closed):
# - Select irradiation time for leakage measurements
# - Measure the electrometer charge
# - Calculate leakage current
#
# 2.2. Kerma measurement (shutter open):
# - Select irradiation time for leakage measurements
# - Measure the electrometer charge
# - Measure pressure (1 barometer)
# - Measure temperature (2 probes connected to the same thermometer)
# - Calculate current intensity (excluding leakages and corrected for reference pressure and temperature conditions)
# - Calculate kerma rate (includes distance factor)
#
# 3. VCV of the operational magnitude rate
# - Kerma rate (calculated previously)
# - Kerma-to-measurement magnitude conversion factor (previously chosen)
# - Electrometer range correction factor (from the reference chamber calibration certificate, RANGE LOW HIGH table,
#   select range)
# - Air density correction factor (read from Hp tab, air attenuation table)
#
# 4. Equipment measurements
# - Equipment background measurements (shutter closed)
# - Equipment readings
# - Measure pressure (only if chamber is open to air)
# - Measure temperature (only if chamber is open to air)
# - Correct for pressure and temperature if chamber is open
# - Correct for equipment background
#
# 5. Calculate dose rate calibration factor
# - VCV of previously calculated magnitude between equipment reading
# - The monitoring chamber is used to verify beam stability
# - Monitoring chamber measurements should be the same when measuring with the reference chamber and when measuring with
#   the equipment because you have the same voltage and current conditions
# - VCV * monitoring chamber measurement when measuring with the equipment
# - Equipment reading * monitoring chamber measurement when measuring with the reference chamber
# - These products are sieverts/hour * current intensity
# - The calibration factor is the relationship between both
#
# 6. Distance factor
# Simultaneous measurements of the reference chamber and the monitoring chamber at two distances
#
# 6.1. Leakage current measurements (shutter closed):
# - Select irradiation time for leakage measurements
# - Measure the electrometer charge
# - Calculate leakage current
#
# 6.2. Current intensity measurement (shutter open):
# - Select irradiation time for leakage measurements
# - Measure the electrometer charge
# - Measure pressure (1 barometer)
# - Measure temperature (2 probes connected to the same thermometer)
# - Calculate current intensity (excluding leakages and corrected to reference pressure and temperature conditions)
#
# 6.3. Calculate distance correction factor
#
# Note: All measurements: 5 measurements in 60 seconds

# ## 1. Initial information
# ----------------------------------------------------------------------------------------------------------------------
# ### 1.1. Reference radiation:

# # Define radiation quality
# radiation_quality = 'L-170'
# print(f'Radiation quality: {radiation_quality}\n')
#
# # ### 1.2. Reference chamber:
#
# # Define reference ionization chamber
# reference_chamber_id = 'ns557'
# reference_chamber_data = '../assets/standard_chambers.json'
#
# with open(reference_chamber_data, 'r') as file:
#     json_data = json.load(file)
#
# reference = IonizationChamber(identification=reference_chamber_id, calibrated=True, open_chamber=True, json_data=json_data)
#
# print(
#     f'Identification: {reference_chamber_id}\n'
#     # f'Electrometer range: {electrometer_range}\n'
#     # f'Electrometer range correction: {electrometer_range_correction}\n'
#     f'Data file: {reference_chamber_data}\n'
# )
#
# # ### 1.3. Environmental conditions:
#
# print(
#     f'Reference temperature: {REFERENCE_TEMPERATURE} ºC\n'
#     f'Reference pressure: {REFERENCE_PRESSURE} kPa\n'
# )
#
# # ### 1.4. Other information
#
# # Define monitor ionization chamber
# monitor_chamber_id = 'monitor'
#
# monitor = IonizationChamber(identification=monitor_chamber_id, calibrated=False, open_chamber=True)
#
# print(f'Monitor chamber ID: {monitor_chamber_id}\n')

# ## 2. Simultaneous measurements of reference chamber and monitor chamber
# ----------------------------------------------------------------------------------------------------------------------

# ### 2.1. Leakage measurements
# ----------------------------------------------------------------------------------------------------------------------

# Measurements of the monitor chamber
# ----------------------------------------------------------------------------------------------------------------------

# Define monitor ionization chamber
monitor_chamber_id = 'monitor'
monitor = IonizationChamber(identification=monitor_chamber_id, calibrated=False, open_chamber=True)

# Readings of the monitor chamber
monitor_leakage_time_readings = np.array([60, 60, 60, 60])
monitor_leakage_charge_readings = np.array([-8.50E-13, -4.30E-13, -2.70E-13, -7.50E-13])
monitor_leakage_pressure_readings = np.array([REFERENCE_PRESSURE] * 4)
monitor_leakage_temperature_readings = np.array([REFERENCE_TEMPERATURE] * 4)

# Define readings units
time_unit = 's'
charge_unit = 'C'
pressure_unit = 'kPa'
temperature_unit = 'ºC'
current_unit = 'A'

# Measure leakage current with the monitor chamber
monitor_leakage_measurement = monitor.measure_current(
    time_readings=monitor_leakage_time_readings, charge_readings=monitor_leakage_charge_readings, time_unit=time_unit,
    charge_unit=charge_unit, temperature_readings=monitor_leakage_temperature_readings,
    pressure_readings=monitor_leakage_pressure_readings, temperature_unit=temperature_unit, pressure_unit=pressure_unit)

print(monitor_leakage_measurement.to_json())
# Export measurements to dataframes
# df_monitor_leakage_measurement = monitor_leakage_measurement.to_dataframe()

# print(f'{df_monitor_leakage_measurement.to_string(index=True)}\n')

# Measurements of the reference chamber
# ----------------------------------------------------------------------------------------------------------------------

# # Readings of the reference chamber
# reference_leakage_time_readings = np.array([60, 60, 60, 60, 60])
# reference_leakage_charge_readings = np.array([-1.00E-14, -1.10E-13, -1.00E-13, 3.00E-14, 0])
#
# # Measure leakage current with the reference chamber
# reference_leakage_measurement = reference.measure_leakage_current(
#     time_readings=reference_leakage_time_readings, charge_readings=reference_leakage_charge_readings, time_unit=time_unit, charge_unit=charge_unit)
#
# # Export measurements to dataframes
# df_reference_leakage_measurement = reference_leakage_measurement.to_dataframe()
#
# # Print results
# print(f'{df_reference_leakage_measurement.to_string(index=True)}\n')

# TODO: If reference and monitor chambers are open, why the environmental correction is not taken in account when measuring leakage current?***

# ### 2.2. Air kerma measurements
# ----------------------------------------------------------------------------------------------------------------------

# Measurements of the monitor chamber
# ----------------------------------------------------------------------------------------------------------------------

# # Readings of the monitor chamber
# monitor_time_readings = np.array([60, 60, 60, 60, 60])
# monitor_pressure_readings = np.array([93.642, 93.642, 93.638, 93.638, 93.633])
# monitor_temperature_readings = np.array([20.63, 20.6, 20.6, 20.6, 20.63])
# monitor_charge_readings = np.array([4.16E-12, 3.54E-12, 4.18E-12, 4.38E-12, 4.36E-12])
#
# # Define readings units
# time_unit = 's'
# charge_unit = 'C'
# pressure_unit = 'kPa'
# temperature_unit = 'ºC'
# current_unit = 'A'
#
# # Measure current with the monitor chamber
# monitor_current_measurement = monitor.measure_current(
#     time_readings=monitor_time_readings, charge_readings=monitor_charge_readings, time_unit=time_unit,
#     charge_unit=charge_unit, background=monitor_leakage_measurement.current.value,
#     temperature_readings=monitor_temperature_readings, pressure_readings=monitor_pressure_readings,
#     current_unit=current_unit, temperature_unit=temperature_unit, pressure_unit=pressure_unit)
#
# # Export measurements to dataframes
# df_monitor_current_measurement = monitor_current_measurement.to_dataframe()
#
# # Print results
# print(f'{df_monitor_current_measurement.to_string(index=True)}\n')

# Measurements of the reference chamber
# ----------------------------------------------------------------------------------------------------------------------

# # Readings of the reference chamber
# reference_time_readings = np.array([60, 60, 60, 60, 60])
# reference_pressure_readings = np.array([93.642, 93.642, 93.638, 93.638, 93.633])
# reference_temperature_readings = np.array([20.88, 20.91, 20.9, 20.94, 20.96])
# reference_charge_readings = np.array([-1.162E-11, -1.168E-11, -1.169E-11, -1.175E-11, -1.164E-11])
#
# # Measure air kerma with the reference chamber
# reference_current_measurement = reference.measure_current(
#     time_readings=reference_time_readings, charge_readings=reference_charge_readings, time_unit=time_unit,
#     charge_unit=charge_unit, background=reference_leakage_measurement.current.value,
#     temperature_readings=reference_temperature_readings, pressure_readings=reference_pressure_readings,
#     current_unit=current_unit, temperature_unit=temperature_unit, pressure_unit=pressure_unit)
# reference_kerma_measurement = reference.measure_air_kerma_rate(
#     current_measurement=reference_current_measurement, radiation_quality=radiation_quality)
#
# # Export measurements to dataframes
# df_reference_kerma_measurement = reference_kerma_measurement.to_dataframe()
#
# # Print results
# print(
#     f'Calibration coefficient: {reference.calibration_coefficients[get_radiation_quality_series(radiation_quality)]}\n'
#     f'Correction factor: {reference.calibration_coefficients_correction[radiation_quality]}\n'
#     f'Distance factor: {0.206378548}\n'  # TODO: Hardcoded value
#     f'{df_reference_kerma_measurement.to_string(index=True)}\n'
# )

# >***QUESTION: Why compute 5 intensities and air kerma readings and not compute it from the mean charge? Uncertainties?***
# >***TO DO: Distance factor value hardcoded. It must be computed.***
# >***TO DO: Small discrepancy in air kerma uncertainty, compare what excel and python functions do to compute the std.***

# ### 2.3. Conventional true value of operational magnitude
# ----------------------------------------------------------------------------------------------------------------------

# # Get kerma rate from ionization chamber measurement
# mean_air_kerma_rate = abs(reference_kerma_measurement.air_kerma_rate.value)
#
# # Define path to radiation quality data file
# conversion_coefficients = '../assets/radiation_quality_data.csv'
# # Read radiation quality data file
# csv_data = pd.read_csv(conversion_coefficients, header=1)
# # Define measurement magnitude
# measurement_magnitude = 'H*(10)'
# # Get kerma-to-measurement magnitude conversion factor from CSV
# conversion_coefficient = csv_data.loc[csv_data['Quality'] == 'L-170', f'h_k[{measurement_magnitude}]'].values[0]
#
# # Define electrometer range
# electrometer_range = 'low'
# # Get electrometer range correction factor from ionization chamber
# electrometer_range_correction = json_data[reference_chamber_id]["electrometer range"][electrometer_range]
#
# # Get air attenuation factor from CSV data
# air_attenuation_coefficient = csv_data.loc[csv_data['Quality'] == 'L-170', 'mu_air'].values[0]
# # Define air width
# air_width = 0.001293
# # Get pressure from ionization chamber measurement
# mean_pressure = reference_kerma_measurement.pressure.value
# # Get temperature from ionization chamber measurement in celsius
# mean_temperature = reference_kerma_measurement.temperature.value
# # Get temperature from ionization chamber measurement in kelvin
# mean_temperature_k = celsius_to_kelvin(reference_kerma_measurement.temperature.value)
# # Change reference temperature units to kelvin
# reference_temperature = celsius_to_kelvin(REFERENCE_TEMPERATURE)
# # Compute air density correction factor
# # air_density_correction = np.exp(
# #     air_attenuation_coefficient * air_width * (mean_pressure / REFERENCE_PRESSURE) * (REFERENCE_TEMPERATURE / mean_temperature_k))
# air_density_correction = np.exp(
#     air_attenuation_coefficient * air_width * (mean_pressure / 101.25) * (273.15 / mean_temperature_k))
# # Compute operational magnitude rate
# ctv_rate = mean_air_kerma_rate * conversion_coefficient * electrometer_range_correction * air_density_correction * hour_to_second(1)
#
# # Compute integration time
# integration_time = sum(reference_kerma_measurement.time_readings)
#
# # Compute integral operational magnitude
# ctv_integral = ctv_rate * integration_time / hour_to_second(1)
#
# # Print results
# print(
#     f'Mean kerma rate: {mean_air_kerma_rate}\n\n'
#     f'Measurement magnitude: {measurement_magnitude}\n'
#     f'Data file: {conversion_coefficients}\n'
#     f'Conversion coefficient: {conversion_coefficient}\n\n'
#     f'Electrometer range: {electrometer_range}\n'
#     f'Electrometer range correction: {electrometer_range_correction}\n\n'
#     f'Air attenuation coefficient correction: {air_attenuation_coefficient}\n'
#     f'Air width: {air_width}\n'
#     f'Mean pressure: {mean_pressure}\n'
#     f'Mean temperature: {mean_temperature}\n'
#     f'Air density correction: {air_density_correction}\n\n'
#     f'CTV of the operational magnitude rate: {ctv_rate}\n'
#     f'Integration time: {integration_time}\n'
#     f'CTV of the integral operational magnitude: {ctv_integral}\n'
# )
#
# ctv = reference.measure_operational_magnitude(
#     kerma_measurement=reference_kerma_measurement,
#     radiation_quality_csv='../assets/radiation_quality_data.csv',
#     measurement_magnitude='H*(10)',
#     radiation_quality='L-170',
#     electrometer_range='low'
# )
# print(ctv)

# >***QUESTION: What happens with the kerma sign (positive or negative)? If current is negative kerma is negative? Or is it always positive?***
# >***QUESTION: When calculating ambient correction in reference chamber intensity readings, reference temperature is 293.15 K (20ºC) and reference pressure is 101.325 kPa (1 atm). However, when calculating air density correction, reference temperature is 273.15 K and reference pressure is 101.25 kPa. The air density correction is 1.00017 in the first case and 1.00016 in the second case. I am going to use the first reference values, but this differs from the spreed sheet. Also, I though that the reference laboratory conditions were 25ºC and 1 atm, we are using 20ºC.***
