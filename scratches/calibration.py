import json

import numpy as np

from src.metpyx.ionization_chamber import IonizationChamber

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

