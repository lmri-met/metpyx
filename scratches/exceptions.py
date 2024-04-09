import warnings


class IonizationChamberException(Exception):
    # Base class for IonizationChamber class exceptions
    pass


class NotCalibratedError(IonizationChamberException):
    # Not calibrated ionization chamber: cannot compute air kerma rate or operational magnitudes
    def __init__(self, magnitude):
        self.msg = 'The ionization chamber is not calibrated.'
        self.magnitude = magnitude

    def __str__(self):
        return f'{self.msg} Cannot compute {self.magnitude}.'


class CurrentMeasurementError(IonizationChamberException):
    def __init__(self, chamber_type, magnitudes, arguments):
        self.chamber_type = chamber_type
        self.magnitudes = magnitudes
        self.arguments = arguments

    def __str__(self):
        return (f'To measure current with a {self.chamber_type} ionization chamber you need to provide the readings '
                f'and unit of {self.magnitudes}. The next arguments are missing {self.arguments}.')


class IonizationChamberWarning(UserWarning):
    pass


def _check_measure_current_arguments(self, time_readings, charge_readings, time_unit, charge_unit,
                                     temperature_readings=None, pressure_readings=None, temperature_unit=None,
                                     pressure_unit=None):
    base_arguments = {
        'time_readings': time_readings,
        'charge_readings': charge_readings,
        'time_unit': time_unit,
        'charge_unit': charge_unit
    }
    environmental_arguments = {
        'temperature_readings': temperature_readings,
        'pressure_readings': pressure_readings,
        'temperature_unit': temperature_unit,
        'pressure_unit': pressure_unit
    }
    if self.open_chamber:
        # Define needed arguments and magnitudes
        needed_arguments = {**base_arguments, **environmental_arguments}
        needed_magnitudes = 'time, charge, temperature and pressure'
    else:
        # Define needed arguments and magnitudes and not needed arguments
        needed_arguments = base_arguments
        needed_magnitudes = 'time and charge'
        not_needed_arguments = environmental_arguments

        # Get a list of not needed arguments that are not None
        not_none_arguments = [key for key, value in not_needed_arguments.items() if value is not None]
        # If there are not needed arguments that are not None, show a warning
        if len(not_none_arguments) > 0:
            message = (f'To measure current with a closed ionization chamber temperature and pressure are not '
                       f'needed. Next arguments will be ignored: {not_none_arguments}')
            warnings.warn(f'{message}', IonizationChamberWarning)

    # Get a list of needed arguments that are None
    none_arguments = [key for key, value in needed_arguments.items() if value is None]
    # If there are needed arguments that are None, raise an Exception
    if len(none_arguments) > 0:
        chamber_type = 'open' if self.open_chamber else 'closed'
        raise CurrentMeasurementError(chamber_type=chamber_type, magnitudes=needed_magnitudes,
                                      arguments=none_arguments)


# Check arguments for the current measuring mode open/close ionization chamber
_check_measure_current_arguments(time_readings, charge_readings, time_unit, charge_unit, temperature_readings,
                                 pressure_readings, temperature_unit, pressure_unit)

# # Check arguments for the current measuring mode with/without background current
# if background:
#     if background_current is None:
#         raise Exception(f'To measure current taking into account the background current you need to provide '
#                         f'the background current value and unit: {background_current}')
# else:
#     if background_current is not None:
#         warnings.warn(f'To measure current not taking into account the background current, the background '
#                       f'current is not used. This argument will be ignored: {background_current}')
