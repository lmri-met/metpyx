# Simulation subpackage design

Subpackage: src/sim

Initial features:

- Spectral simulation: Compute spectra and integral quantities (some of them using SpekPy).
- High voltage sensitivity: Perform sensitivity analysis on spectra and integral quantities due to variations in tube
  high voltage.
- Filtration thickness sensitivity: Perform sensitivity analysis on spectra and integral quantities due to variations in
  additional filtration thickness.
- Filtration purity sensitivity: Perform sensitivity analysis on spectra and integral quantities due to variations in
  additional filtration purity.

## Feature 1: Spectral simulation

Class: Quality
Module: src/metpyx/sim/PLACEHOLDER.py

**IMPORTANT: Quality class do not work with spekpy 2.5.3. Please use spekpy 2.0.13.**

Initialization:

- This class will receive as argument the name of an x-ray radiation quality (e.g. "N60").
- The class will use src/metpyx/data/qualities.py to retrieve the parameters of the quality (i.e. high voltage and total
filtration).
- Then it will create a Spek object from SpekPy using these parameters.
- The class need to convert the total filtration into the appropriate format for SpekPy.

Computing SpekPy Spectrum and integral quantities:
- The class inherits from SpekPy Spek class.
- Therefore, it can use all the methods from SpekPy Spek class to compute the spectrum and integral quantities.
- The only integral quantities it cannot compute are the ones that depend on air kerma to fluence conversion coefficients (mean conversion coefficient and operational quantities).

Computing mean conversion coefficient:

## Notes about SpekPy

Example usage of SpekPy to generate and filter an X-ray spectrum:

All keywords for Spek class (all are optional):

- kvp = 90 # Tube potential in kV (default: 100)
- th = 14 # Anode angle in degrees (default: 12)
- dk = 1.0 # Spectrum bin width in keV (default: 0.5)
- physics = "legacy" # Legacy physics mode rather than default (default: "default")
- mu_data_source = "pene" # Penelope mu/mu_en data rather than NIST/XCOM (default: "nist")
- z = 75 # Point-of-interest is at a focus-to-detector-distance of 75 cm (default: 100)
- x = 5 # Point-of-interest displaced 5 cm towards cathode in anode-cathode direction (default: 0)
- y = -5 # Point-of-interest displaced -5 cm in orthogonal direction (right-hand-rule is applicable) (default: 0)
- mas = 2 # Exposure set to 2 mAs (default: 1)
- brem = True # Whether the bremsstrahlung portion of spectrum is retained (default: True)
- char = False # Whether the characteristic portion of spectrum is retained (default: True)
- obli = False # Whether path-length through extrinsic filtration varies with x, y (default: True)

Generate unfiltered spectrum:

s = sp.Spek(kvp=kvp, th=th, dk=dk, physics=physics, mu_data_source=mu_data_source, x=x, y=y, z=z, mas=mas, brem=brem,
char=char, obli=obli)

Mutli-filter the spectrum:

added_filtration=[ ['Al',4.0], ['Air',1000] ]
s.multi_filter(added_filtration)

Get relevant integral quantities:

- print('Mean energy of spectrum:', s.get_emean(), 'keV')
- print('Air kerma:', s.get_kerma(), 'uGy')
- print('1st Hvl:', s.get_hvl1(), 'mm Al')
- print('2nd Hvl:', s.get_hvl2(), 'mm Al')
- print('1st Hvl:', s.get_hvl1(matl='Cu'), 'mmCu')
- print('2nd Hvl:', s.get_hvl2(matl='Cu'), 'mmCu')
