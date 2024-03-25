import json

import src.metpyx.calibration as cal

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

# CLASS: IONIZATION CHAMBER

# Define standard ionization chamber
ic = cal.IonizationChamber(identification='monitor')

# Measure leak current
leak_time_readings = [60, 60, 60, 60, 0]
leak_charge_readings = [-8.50E-13, -4.30E-13, -2.70E-13, -7.50E-13, 0]
leak_current_series = ic.measure_current_series(time_readings=leak_time_readings, charge_readings=leak_charge_readings)
leak_current_magnitude = ic.measure_current(time_readings=leak_time_readings, charge_readings=leak_charge_readings)

# Measure current
time_readings = [60, 60, 60, 60, 60]
charge_readings = [4.16E-12, 3.54E-12, 4.18E-12, 4.38E-12, 4.36E-12]
temperature_readings = [20.63, 20.6, 20.6, 20.6, 20.63]
pressure_readings = [93.642, 93.642, 93.638, 93.638, 93.633]
current_series = ic.measure_ambient_corrected_current_series(
    charge_readings=charge_readings, time_readings=time_readings, leak_current_value=leak_current_magnitude.value,
    temperature_readings=temperature_readings, pressure_readings=pressure_readings)
current = ic.measure_ambient_corrected_current(
    charge_readings=charge_readings, time_readings=time_readings, leak_current_value=leak_current_magnitude.value,
    temperature_readings=temperature_readings, pressure_readings=pressure_readings)

# Complete current measurement
series_df, magnitudes_df = ic.detail_current_measurement(leak_charge_readings, leak_time_readings, charge_readings,
                                                         time_readings, temperature_readings, pressure_readings)

# Print results
print('Monitor chamber measurements')
print(series_df)
print(magnitudes_df)

# TODO: issue with building series dataframes: leak readings are only four, while current readings are five.
#  If we fill with zeros, leak current returns nan and current cannot be calculated

# CLASS: STANDARD IONIZATION CHAMBER

# # Read standard ionization chamber calibration coefficients and correction factors
# with open('assets/standard_chambers.json', 'r') as file:
#     data = json.load(file)
# standard_chamber_calibration_coefficients = data['ns557']['calibration coefficient']
# standard_chamber_corrector_factors = data['ns557']['correction factor']
#
# # Define standard ionization chamber
# sic = cal.StandardIonizationChamber(
#     identification='ns557',
#     calibration_coefficients=standard_chamber_calibration_coefficients,
#     correction_factors=standard_chamber_corrector_factors
# )
#
# # Leak measurement
# leak_time = [60, 60, 60, 60, 60]
# leak_charge = [-1.00E-14, -1.10E-13, -1.00E-13, 3.00E-14, 0]
# leak_current_series = sic.measure_current_series(time=leak_time, charge=leak_charge)
# leak_current = sic.measure_current(time=leak_time, charge=leak_charge)
#
# # Current measurement
# time = [60, 60, 60, 60, 60]
# pressure = [93.642, 93.642, 93.638, 93.638, 93.633]
# temperature = [20.88, 20.91, 20.9, 20.94, 20.96]
# charge = [-1.162E-11, -1.168E-11, -1.169E-11, -1.175E-11, -1.164E-11]
# current_series = sic.measure_ambient_corrected_current_series(charge=charge, time=time, leak_current=leak_current.value,
#                                                               temperature=temperature, pressure=pressure)
# current = sic.measure_ambient_corrected_current(charge=charge, time=time, leak_current=leak_current.value,
#                                                 temperature=temperature, pressure=pressure)
#
# # Air kerma measurement
# # TODO: small discrepancy in uncertainty, compare what excel and python functions to compute the standard deviation do)
# radiation_quality = 'L-170'
# air_kerma_series = sic.measure_air_kerma_series(current=current_series, radiation_quality=radiation_quality)
# air_kerma = sic.measure_air_kerma(current=current_series, radiation_quality=radiation_quality)
#
# # Complete current measurement
# series_df, magnitudes_df = sic.detail_current_measurement(leak_charge, leak_time, charge, time, temperature, pressure)
#
# # Print results
# print('Standard chamber measurements')
# print(series_df)
# print(magnitudes_df)
