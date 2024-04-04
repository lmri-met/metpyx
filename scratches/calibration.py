import json

import numpy as np

from src.metpyx.ionization_chamber import IonizationChamber, REFERENCE_PRESSURE, REFERENCE_TEMPERATURE, get_radiation_quality_series

# STEP 1: Simultaneous measurements of the reference chamber and the monitoring chamber

# Leakage current measurements

# Define monitor ionization chamber
monitor_chamber_id = 'monitor'
monitor = IonizationChamber(identification=monitor_chamber_id, calibrated=False, open_chamber=True)

# Define reference ionization chamber
reference_chamber_id = 'ns557'
reference_chamber_data = '../assets/standard_chambers.json'
with open(reference_chamber_data, 'r') as file:
    json_data = json.load(file)
reference = IonizationChamber(identification=reference_chamber_id, calibrated=True, open_chamber=True,
                              json_data=json_data)
# Readings of the monitor chamber
monitor_leakage_time_readings = np.array([60, 60, 60, 60])
monitor_leakage_charge_readings = np.array([-8.50E-13, -4.30E-13, -2.70E-13, -7.50E-13])

# Readings of the reference chamber
reference_leakage_time_readings = np.array([60, 60, 60, 60, 60])
reference_leakage_charge_readings = np.array([-1.00E-14, -1.10E-13, -1.00E-13, 3.00E-14, 0])

# Define readings units
time_unit = 's'
charge_unit = 'C'

# Measure leakage current with the monitor chamber
monitor_leakage_measurement = monitor.measure_leakage_current(
    time_readings=monitor_leakage_time_readings, charge_readings=monitor_leakage_charge_readings,
    time_unit=time_unit, charge_unit=charge_unit)

# Measure leakage current with the reference chamber
reference_leakage_measurement = reference.measure_leakage_current(
    time_readings=reference_leakage_time_readings, charge_readings=reference_leakage_charge_readings,
    time_unit=time_unit, charge_unit=charge_unit)

# Export measurements to dataframes
df_monitor_leakage_measurement = monitor_leakage_measurement.to_dataframe()
df_reference_leakage_measurement = reference_leakage_measurement.to_dataframe()

# Air kerma measurements

# Define radiation quality
radiation_quality = 'L-170'

# Define readings units
time_unit = 's'
charge_unit = 'C'
pressure_unit = 'kPa'
temperature_unit = 'ºC'
current_unit = 'A'


# Readings of the monitor chamber
monitor_time_readings = np.array([60, 60, 60, 60, 60])
monitor_pressure_readings = np.array([93.642, 93.642, 93.638, 93.638, 93.633])
monitor_temperature_readings = np.array([20.63, 20.6, 20.6, 20.6, 20.63])
monitor_charge_readings = np.array([4.16E-12, 3.54E-12, 4.18E-12, 4.38E-12, 4.36E-12])

# Readings of the reference chamber
reference_time_readings = np.array([60, 60, 60, 60, 60])
reference_pressure_readings = np.array([93.642, 93.642, 93.638, 93.638, 93.633])
reference_temperature_readings = np.array([20.88, 20.91, 20.9, 20.94, 20.96])
reference_charge_readings = np.array([-1.162E-11, -1.168E-11, -1.169E-11, -1.175E-11, -1.164E-11])

# Measure current with the monitor chamber
monitor_current_measurement = monitor.measure_current(
    time_readings=monitor_time_readings, charge_readings=monitor_charge_readings, time_unit=time_unit,
    charge_unit=charge_unit, background=monitor_leakage_measurement.current.value,
    temperature_readings=monitor_temperature_readings, pressure_readings=monitor_pressure_readings,
    current_unit=current_unit, temperature_unit=temperature_unit, pressure_unit=pressure_unit)

# Measure air kerma with the reference chamber
reference_current_measurement = reference.measure_current(
    time_readings=reference_time_readings, charge_readings=reference_charge_readings, time_unit=time_unit,
    charge_unit=charge_unit, background=reference_leakage_measurement.current.value,
    temperature_readings=reference_temperature_readings, pressure_readings=reference_pressure_readings,
    current_unit=current_unit, temperature_unit=temperature_unit, pressure_unit=pressure_unit)
reference_kerma_measurement = reference.measure_air_kerma_rate(
    current_measurement=reference_current_measurement, radiation_quality=radiation_quality)

# Export measurements to dataframes
df_monitor_current_measurement = monitor_current_measurement.to_dataframe()
df_reference_kerma_measurement = reference_kerma_measurement.to_dataframe()

# FINAL STEP: Results report
output_file = './output.txt'
results = (
    f'IR-14D: Calibration of radiation measuring devices\n'
    f'\n'
    f'INITIAL INFORMATION\n'
    f'\n'
    f'Reference radiation:\n'
    # f'Radiation quality series: {radiation_quality_series}\n'
    f'Radiation quality: {radiation_quality}\n'
    # f'Air attenuation coefficient: {air_attenuation_coefficient}\n'
    # f'Conversion coefficient: {conversion_coefficient}'
    # f'Data file: {conversion_coefficients}\n'
    f'\n'
    f'Reference chamber:\n'
    f'Identification: {reference_chamber_id}\n'
    # f'Electrometer range: {electrometer_range}\n'
    # f'Electrometer range correction: {electrometer_range_correction}\n'
    f'Data file: {reference_chamber_data}\n'
    f'\n'
    f'Environmental conditions:\n'
    f'Reference temperature: {REFERENCE_TEMPERATURE} ºC\n'
    f'Reference pressure: {REFERENCE_PRESSURE} kPa\n'
    f'\n'
    f'Other information\n'
    # f'Measurement magnitude: {measurement_magnitude}\n'
    f'Monitor chamber ID: {monitor_chamber_id}\n'
    # f'Detector ID: {detector}\n'
    # f'Celsius to Kelvin conversion: {celsius_to_kelvin}\n'
    # f'Hour to seconds conversion: {hour_to_second}\n'
    f'\n'
    f'SIMULTANEOUS MEASUREMENTS OF REFERENCE CHAMBER AND MONITOR CHAMBER\n'
    f'\n'
    f'Leakage measurements\n'
    f'\n'
    f'Measurements of the monitor chamber\n'
    f'{df_monitor_leakage_measurement.to_string(index=True)}\n'
    f'\n'
    f'Measurements of the reference chamber\n'
    f'{df_reference_leakage_measurement.to_string(index=True)}\n'
    f'\n'
    f'Air kerma measurements\n'
    f'\n'
    f'Measurements of the monitor chamber\n'
    f'{df_monitor_current_measurement.to_string(index=True)}\n'
    f'\n'
    f'Measurements of the reference chamber\n'
    f'Calibration coefficient: {reference.calibration_coefficients[get_radiation_quality_series(radiation_quality)]}\n'
    f'Correction factor: {reference.calibration_coefficients_correction[radiation_quality]}\n'
    f'Distance factor: {0.206378548}\n'  # TODO: Hardcoded value
    f'{df_reference_kerma_measurement.to_string(index=True)}\n'
    f'\n'
    # f'CTV of the operational magnitude rate\n'
    # f'Mean air kerma rate: {mean_air_kerma_rate}\n'
    # f'Conversion coefficient: {conversion_coefficient}\n'
    # f'Electrometer range correction: {electrometer_range_correction}\n'
    # f'Air density correction: {air_density_correction}\n'
    # f'CTV of the operational magnitude rate: {ctv_rate}\n'
    # f'Integration time: {integration_time}\n'
    # f'CTV of the integral operational magnitude: {ctv_integral}\n'
    # f'\n'
)
with open(output_file, 'w') as f:
    f.write(results)
print(f'Calibration results written to {output_file}')
