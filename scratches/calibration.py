import json

import numpy as np

from src.metpyx.ionization_chamber import IonizationChamber

# Simultaneous measurements of the reference chamber and the monitoring chamber

# Measurements of the reference chamber

# Leakage current measurements

# Define reference ionization chamber
reference_chamber_id = 'ns557'
reference_chamber_data = '../assets/standard_chambers.json'
with open(reference_chamber_data, 'r') as file:
    json_data = json.load(file)
reference = IonizationChamber(identification=reference_chamber_id, calibrated=True, open_chamber=True,
                              json_data=json_data)
# Measure leakage current
leakage_time_readings = np.array([60, 60, 60, 60, 60])
leakage_charge_readings = np.array([-1.00E-14, -1.10E-13, -1.00E-13, 3.00E-14, 0])
leakage_measurement = reference.measure_leakage_current(time_readings=leakage_time_readings,
                                                        charge_readings=leakage_charge_readings, time_unit='s',
                                                        charge_unit='C')
