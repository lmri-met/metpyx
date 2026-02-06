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
- The only integral quantities it cannot compute are the ones that depend on air kerma to fluence conversion
  coefficients (mean conversion coefficient and operational quantities).

Computing mean conversion coefficient:

- The class will have a method to compute the mean conversion coefficient.
- To compute the mean conversion coefficient, we need:
    - the spectrum
    - the mono-energetic conversion coefficients
    - the mono-energetic mass transfer coefficients of air
- The spectrum is obtained from SpekPy Spek class.
- The mono-energetic conversion coefficients for each quantity and irradiation angle:
    - will be stored in the data subpackage
    - Provide the most recent ones from CMI 2025 as default, and let the user add others if needed.
- The mono-energetic mass transfer coefficients of air:
    - will be stored in the data subpackage
    - Provide those from PENELOPE v. 2018, and let the user add others if needed.

## Notes abouts computing mean conversion coeffcient in USpekPy
def get_mean_conversion_coefficient(self, mass_transfer_coefficients, conversion_coefficients, angle=None):
  """Compute the mean conversion coefficient of an x-ray spectrum in Sv/Gy.

  This method calculates the mean conversion coefficient of an x-ray spectrum using the photon fluence energy
  distribution, the mass energy transfer coefficients of air and the air kerma-to-dose-equivalent
  monoenergetic conversion coefficients. The steps are:
  - Obtain the spectrum energy and fluence using the `get_spectrum` method.
  - Unpack the energies and values of the mass energy transfer coefficients and the monoenergetic conversion
    coefficients.
  - Interpolate the mass energy transfer coefficients of air and the monoenergetic conversion coefficients for the
    spectrum energies in logarithmic scale using the `interpolate` function.
  - Compute the mean conversion coefficient. It first computes the sum of the product of the fluence, energy,
    interpolated mass energy transfer coefficients and interpolated conversion coefficients in each energy bin.
    Then, it computes the sum of the product of the fluence, energy and interpolated mass energy transfer
    coefficients in each energy bin. Finally, it divides the first sum of products by the second sum of products.

  Args:
      mass_transfer_coefficients (tuple): Tuple containing the energies and values of the mass energy transfer
          coefficients of air (keV, cm²/g).
      conversion_coefficients (tuple): Tuple containing the energies and values of the monoenergetic conversion
          coefficients (keV, Sv/Gy).
      angle (float, optional): The radiation incidence angle at which the mean conversion coefficient is
          calculated.

  Returns:
      float: The mean conversion coefficient computed.
  """
  Get spectrum energy and fluence (keV, 1/cm²)
  energy, fluence = self.get_spectrum(diff=False)

  Unpack the energies and values of the mass energy transfer coefficients of air (keV, cm²/g)
  energy_mu, mu = parse_mass_transfer_coefficients(mass_transfer_coefficients)

  Unpack the energies and values of the monoenergetic conversion coefficients (keV, Sv/Gy)
  energy_hk, hk = parse_conversion_coefficients(conversion_coefficients, angle)

  Interpolate mass energy transfer coefficients of air for the spectrum energies in logarithmic scale
  interpolated_mu = interpolate(x=energy_mu, y=mu, new_x=energy)

  Interpolate monoenergetic conversion coefficients for the spectrum energies in logarithmic scale
  interpolated_hk = interpolate(x=energy_hk, y=hk, new_x=energy)

  Compute the mean conversion coefficient (Sv/Gy)
  return sum(fluence * energy * interpolated_mu * interpolated_hk) / sum(fluence * energy * interpolated_mu)

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
