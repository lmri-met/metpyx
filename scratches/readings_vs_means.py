import numpy as np

pm = chr(177)

# Reference chamber measurements: leakage current measurements

# Readings
leakage_time_readings = np.array([60, 60, 60, 60])
leakage_charge_readings = np.array([-1.00E-14, -1.10E-13, -1.00E-13, 3.00E-14])

# Compute leakage current from leakage current readings
leakage_current_readings = leakage_charge_readings / leakage_time_readings
mean_leakage_current = leakage_current_readings.mean()
mean_leakage_current_std = np.std(leakage_current_readings) / np.sqrt(len(leakage_current_readings))
mean_leakage_current_ru = mean_leakage_current_std / mean_leakage_current * 100

# Compute leakage current from mean leakage charge
mean_leakage_time = leakage_time_readings.mean()
mean_leakage_time_std = np.std(leakage_time_readings) / np.sqrt(len(leakage_time_readings))
mean_leakage_time_ru = mean_leakage_time_std / mean_leakage_time * 100

mean_leakage_charge = leakage_charge_readings.mean()
mean_leakage_charge_std = np.std(leakage_charge_readings) / np.sqrt(len(leakage_time_readings))
mean_leakage_charge_ru = mean_leakage_charge_std / mean_leakage_charge * 100

leakage_current = mean_leakage_charge / mean_leakage_time
leakage_charge_ru = np.sqrt(mean_leakage_time_ru ** 2 + mean_leakage_charge_ru ** 2)
leakage_current_std = leakage_current * leakage_charge_ru / 100

# Comparison
print('Reference chamber: Leakage current:')
print(f'Leakage time: {leakage_time_readings}')
print(f'Leakage charge: {leakage_charge_readings}')
print(f'From readings: {mean_leakage_current} {pm} {mean_leakage_current_std} A ({mean_leakage_current_ru}%)')
print(f'From mean: {leakage_current} {pm} {leakage_current_std} A ({leakage_charge_ru}%)')

# Reference chamber measurements: current measurements

# Readings
time_readings = np.array([60, 60, 60, 60, 60])
pressure_readings = np.array([93.642, 93.642, 93.638, 93.638, 93.633])
temperature_readings = np.array([20.88, 20.91, 20.9, 20.94, 20.96])
charge_readings = np.array([-1.162E-11, -1.168E-11, -1.169E-11, -1.175E-11, -1.164E-11])

# Data
reference_pressure = 101.325
reference_temperature = 20

# Compute current from current readings
environmental_correction_readings = (reference_pressure / reference_temperature) * (temperature_readings / pressure_readings)
mean_environmental_correction = environmental_correction_readings.mean()
mean_environmental_correction_std = np.std(environmental_correction_readings) / np.sqrt(len(environmental_correction_readings))
mean_environmental_correction_ru = mean_environmental_correction_std / mean_environmental_correction * 100

current_readings = (charge_readings / time_readings - mean_leakage_current) * environmental_correction_readings
mean_current = current_readings.mean()
mean_current_std = np.std(current_readings) / np.sqrt(len(current_readings))
mean_current_ru = mean_current_std / mean_current * 100

# Compute current from mean charge
mean_time = time_readings.mean()
mean_time_std = np.std(time_readings) / np.sqrt(len(time_readings))
mean_time_ru = mean_time_std / mean_time * 100

mean_charge = charge_readings.mean()
mean_charge_std = np.std(charge_readings) / np.sqrt(len(charge_readings))
mean_charge_ru = mean_charge_std / mean_charge * 100

mean_pressure = pressure_readings.mean()
mean_pressure_std = np.std(pressure_readings) / np.sqrt(len(pressure_readings))
mean_pressure_ru = mean_pressure_std / mean_pressure * 100

mean_temperature = temperature_readings.mean()
mean_temperature_std = np.std(temperature_readings) / np.sqrt(len(temperature_readings))
mean_temperature_ru = mean_temperature_std / mean_temperature * 100

environmental_correction = (reference_pressure / reference_temperature) * (mean_temperature / mean_pressure)
environmental_correction_ru = np.sqrt(mean_temperature_ru ** 2 + mean_pressure_ru ** 2)
environmental_correction_std = environmental_correction * environmental_correction_ru / 100

current = (mean_charge / mean_time - leakage_current) * environmental_correction
current_std = np.sqrt((environmental_correction / mean_time * mean_charge_std) ** 2 + (
        environmental_correction * mean_charge / mean_time ** 2 * mean_time_std) ** 2 + (
                              environmental_correction * leakage_current_std) ** 2 + (
                                  current / environmental_correction * environmental_correction_std) ** 2)
current_ru = current_std / current * 100

# Comparison
print('Reference chamber: Current:')
print(f'Time: {time_readings}')
print(f'Charge: {charge_readings}')
print(f'Pressure: {pressure_readings}')
print(f'Temperature: {temperature_readings}')
print(f'From readings: {mean_current} {pm} {mean_current_std} A ({mean_current_ru}%)')
print(f'From mean: {current} {pm} {current_std} A ({current_ru}%)')

