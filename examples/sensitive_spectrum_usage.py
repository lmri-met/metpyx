from metpyx import SensitiveSpectrum

# Two ways to initialize the SensitiveSpectrum class:
# Initialize an SensitiveSpectrum object with a quality:
s1 = SensitiveSpectrum(quality='N60')
# Initialize an SensitiveSpectrum object with high voltage, anode angle and filtration:
s2 = SensitiveSpectrum(voltage=60, anode=20, filtration=[('Al', 4), ('Cu', 0.6), ('Air', 1000)])
