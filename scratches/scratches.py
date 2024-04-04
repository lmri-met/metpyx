import numpy as np

pm = chr(177)

# Reference chamber measurements: leakage current measurements

# Readings
leakage_time_readings = np.array([60, 60, 60, 60, 60])
leakage_charge_readings = np.array([-1.00E-14, -1.10E-13, -1.00E-13, 3.00E-14, 0])

# Compute leakage current from leakage current readings
leakage_current_readings = leakage_charge_readings / leakage_time_readings
mean_leakage_current = leakage_current_readings.mean()
mean_leakage_current_std = np.std(leakage_current_readings) / np.sqrt(len(leakage_current_readings))
mean_leakage_current_ru = abs(mean_leakage_current_std / mean_leakage_current * 100)

print('Reference chamber: Leakage current:')
print(f'Leakage time: {leakage_time_readings}')
print(f'Leakage charge: {leakage_charge_readings}')
print(f'Leakage current: {mean_leakage_current} {pm} {mean_leakage_current_std} A ({mean_leakage_current_ru}%)')

# Reference chamber measurements: current measurements

# Readings
time_readings = np.array([60, 60, 60, 60, 60])
pressure_readings = np.array([93.642, 93.642, 93.638, 93.638, 93.633])
temperature_readings = np.array([20.88, 20.91, 20.9, 20.94, 20.96])
charge_readings = np.array([-1.162E-11, -1.168E-11, -1.169E-11, -1.175E-11, -1.164E-11])

# Data
reference_pressure = 101.325
reference_temperature = 20

# Temperature units to kelvin
reference_temperature_k = reference_temperature + 273.15
temperature_readings_k = temperature_readings + 273.15

# Compute current from current readings
environmental_correction_readings = (reference_pressure / reference_temperature_k) * (temperature_readings_k / pressure_readings)
mean_environmental_correction = environmental_correction_readings.mean()
mean_environmental_correction_std = np.std(environmental_correction_readings) / np.sqrt(len(environmental_correction_readings))
mean_environmental_correction_ru = mean_environmental_correction_std / mean_environmental_correction * 100

current_readings = (charge_readings / time_readings - mean_leakage_current) * environmental_correction_readings
mean_current = current_readings.mean()
mean_current_std = np.std(current_readings) / np.sqrt(len(current_readings))
mean_current_ru = abs(mean_current_std / mean_current * 100)

# Comparison
print('Reference chamber: Current:')
print(f'Time: {time_readings}')
print(f'Charge: {charge_readings}')
print(f'Pressure: {pressure_readings}')
print(f'Temperature: {temperature_readings}')
print(f'Current: {current_readings}')
print(f'Current: {mean_current} {pm} {mean_current_std} A ({mean_current_ru}%)')

print('Reference chamber: Air kerma:')
