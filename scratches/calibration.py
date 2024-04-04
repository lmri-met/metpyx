import json

import numpy as np

from src.metpyx.ionization_chamber import IonizationChamber, REFERENCE_PRESSURE, REFERENCE_TEMPERATURE

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

# FINAL STEP: Results report
# -------
output_file = './output.txt'
results = (
    f'IR-14D: Calibration of radiation measuring devices\n'
    f'\n'
    f'INITIAL INFORMATION\n'
    f'\n'
    # f'Reference radiation:\n'
    # f'Radiation quality series: {radiation_quality_series}\n'
    # f'Radiation quality: {radiation_quality}\n'
    # f'Air attenuation coefficient: {air_attenuation_coefficient}\n'
    # f'Conversion coefficient: {conversion_coefficient}'
    # f'Data file: {conversion_coefficients}\n'
    # f'\n'
    f'Reference chamber:\n'
    f'Identification: {reference_chamber_id}\n'
    # f'Calibration coefficient: {calibration_coefficient}\n'
    # f'Correction factor: {correction_factor}\n'
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
    # f'Distance factor: {0.206378548} (WARNING! Hardcoded value)\n'  # TODO: Hardcoded value
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
