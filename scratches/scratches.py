# import numpy as np
#
# pm = chr(177)
#
# # Readings
# time_readings = np.array([60, 60, 60, 60, 60])
# charge_readings = np.array([-1.00E-14, -1.10E-13, -1.00E-13, 3.00E-14, 0])
# pressure_readings = np.array([93.642, 93.642, 93.638, 93.638, 93.633])
# temperature_readings = np.array([20.88, 20.91, 20.9, 20.94, 20.96])
#
# # Data
# reference_pressure = 101.325
# reference_temperature = 20
#
# # Temperature units to kelvin
# reference_temperature_k = reference_temperature + 273.15
# temperature_readings_k = temperature_readings + 273.15
#
# # Compute leakage current measurements with no ambient correction
# current_readings_nec = charge_readings / time_readings
# mean_current_nec = current_readings_nec.mean()
# mean_current_std_nec = np.std(current_readings_nec) / np.sqrt(len(current_readings_nec))
# mean_current_ru_nec = abs(mean_current_std_nec / mean_current_nec * 100)
#
# # Compute leakage current measurements with ambient correction
# environmental_correction_readings = (reference_pressure / reference_temperature_k) * (temperature_readings_k / pressure_readings)
# mean_environmental_correction = environmental_correction_readings.mean()
# mean_environmental_correction_std = np.std(environmental_correction_readings) / np.sqrt(len(environmental_correction_readings))
# mean_environmental_correction_ru = mean_environmental_correction_std / mean_environmental_correction * 100
#
# current_readings_ec = (charge_readings / time_readings) * environmental_correction_readings
# mean_current_ec = current_readings_ec.mean()
# mean_current_std_ec = np.std(current_readings_ec) / np.sqrt(len(current_readings_ec))
# mean_current_ru_ec = abs(mean_current_std_ec / mean_current_ec * 100)
#
# # Comparison
# print('Comparison of leakage current measurement with and without environmental correction')
# print()
# print(f'Time: {time_readings}')
# print(f'Charge: {charge_readings}')
# print(f'Pressure: {pressure_readings}')
# print(f'Temperature: {temperature_readings}')
# print(f'Reference pressure: {reference_pressure}')
# print(f'Reference temperature: {reference_temperature}')
# print(f'Environmental correction: {mean_environmental_correction} {pm} {mean_environmental_correction_std} A ({mean_environmental_correction_ru}%)')
# print()
# print('Leakage current with no ambient correction:')
# print(f'Current: {current_readings_nec}')
# print(f'Current: {mean_current_nec} {pm} {mean_current_std_nec} A ({mean_current_ru_nec}%)')
# print()
# print('Leakage current with ambient correction:')
# print(f'Current: {current_readings_ec}')
# print(f'Current: {mean_current_ec} {pm} {mean_current_std_ec} A ({mean_current_ru_ec}%)')
# print()
# print(mean_current_ec/mean_current_nec)


# class IonizationChamberException(Exception):
#     # Base class for IonizationChamber class exceptions
#     pass
#
#
# class NotCalibratedError(IonizationChamberException):
#     # Not calibrated ionization chamber: cannot compute air kerma rate or operational magnitudes
#     def __init__(self, magnitude):
#         self.msg = 'The ionization chamber is not calibrated.'
#         self.magnitude = magnitude
#
#     def __str__(self):
#         return f'{self.msg} Cannot compute {self.magnitude}.'
#
#
# if __name__ == '__main__':
#     raise NotCalibratedError(magnitude='air kerma rate')
# class CurrentMeasurementError(IonizationChamberException):
#     def __init__(self, chamber_type, magnitudes, arguments):
#         self.chamber_type = chamber_type
#         self.magnitudes = magnitudes
#         self.arguments = arguments
#
#     def __str__(self):
#         return (f'To measure current with a {self.chamber_type} ionization chamber you need to provide the readings '
#                 f'and unit of {self.magnitudes}. The next arguments are missing {self.arguments}.')
#
#
# open_chamber = False
# arguments = {
#     'time readings': 1,
#     'charge readings': None,
#     'time unit': 's',
#     'charge unit': None
# }
# none_arguments = [key for key, value in arguments.items() if value is None]
# if len(none_arguments) > 0:
#     chamber_type = 'open' if open_chamber else 'closed'
#     magnitudes = 'time and charge'
#     arguments = none_arguments
#     raise CurrentMeasurementError(chamber_type, magnitudes, arguments)
# magnitude = 'current'
# magnitude = 'air kerma rate'
# magnitude = 'operational magnitude'
# print(magnitude in ['current', 'air kerma rate', 'operational magnitude'])


class AllMyFields:
    def __init__(self, dictionary):
        for k, v in dictionary.items():
            setattr(self, k, v)


o = AllMyFields({'a': 1, 'b': 2})
print(o.a)
