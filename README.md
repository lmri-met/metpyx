# metpyx: A collection of tools for x-ray metrology

![Static Badge](https://img.shields.io/badge/Date-Jul_24-teal)
![Static Badge](https://img.shields.io/badge/Version-1.0.0-teal)
![Static Badge](https://img.shields.io/badge/Maintenance-Active-teal)

[![Static Badge](https://img.shields.io/badge/Surce_code-GitHub-blue)](https://github.com/lmri-met/metpyx)
[![Static Badge](https://img.shields.io/badge/Documentation-README-blue)](https://github.com/lmri-met/metpyx#README)
[![Static Badge](https://img.shields.io/badge/Contribute-Issues-blue)](https://github.com/lmri-met/metpyx/issues)
[![Static Badge](https://img.shields.io/badge/Organization-LMRI--Met-blue)](https://github.com/lmri-met/)

[![Static Badge](https://img.shields.io/badge/Distribution-PyPi-orange)](https://pypi.org/project/metpyx/)
[![Static Badge](https://img.shields.io/badge/License-GPLv3.0-orange)](https://choosealicense.com/licenses/gpl-3.0/)
![Static Badge](https://img.shields.io/badge/Tests-Passing-green)
![Static Badge](https://img.shields.io/badge/CodeCov-100%25-green)

> **WARNING!: Currently working to add new feature to simulate x-ray spectrum with sensitivity analysis.**

## Table of Contents

- [What is MetPyX?](#what-is-metpyx)
- [Main features of MetPyX](#main-features-of-metpyx)
- [How to install MetPyX?](#how-to-install-metpyx)
- [Quick user guide](#quick-user-guide)
  - [Managing x-ray radiation qualities](#managing-x-ray-radiation-qualities)
  - [Managing x-ray operational quantities](#managing-x-ray-operational-quantities)
- [Future developments](#future-developments)
- [How to get support?](#how-to-get-support)
- [Documentation](#documentation)
- [Contributors](#contributors)
- [License](#license)
- [Contributing to MetPyX](#contributing-to-metpyx)

## What is MetPyX?

**MetPyX** is a collection of tools for x-ray metrology.
**X-ray metrology laboratories** need to deal daily with a wide set of x-ray radiation qualities, 
the filtration thicknesses to get each one of those qualities,
and the operational magnitudes for radiation protection.
**MetPyX** provide tools to ease the management all of them.
It is an open source, GPLv3-licensed library for the Python programming language.
It is compatible with Python 3.

## Main features of MetPyX

**MetPyX** provides two features:
- **Manage x-ray radiation qualities and their corresponding filtration thicknesses**.
  With MetPyX you can:
  get the x-ray radiation quality series or the radiation qualities of a specific series,
  check if a series/quality is an x-ray radiation series/quality,
  get the radiation qualities of a radiation quality series, and
  get the series, peak kilovoltage or filtration thicknesses from a specific radiation quality.
- **Manage x-ray operational quantities for radiation protection and their corresponding irradiation angles**.
  With MetPyX you can
  get the operational quantities for x-rays,
  check if a quantity is an operational quantity for x-rays, and
  get the irradiation angles for an operational quantity.

## How to install MetPyX?

**MetPyX** can be installed from the [Python Package Index (PyPI)](https://pypi.org/project/metpyx/) 
by running the following command from a terminal:

```bash
pip install metpyx
```

## Quick user guide

### Managing x-ray radiation qualities

The tool that **MetPyX** provides to manage x-ray radiation qualities is the **XrayQualities** class.
With **XrayQualities** class you can:
- List the X-ray radiation quality series or the radiation qualities of a specific series.
- Check if a series/quality is an x-ray radiation series/quality.
- Retrieve the radiation qualities of a radiation quality series.
- Retrieve the series, peak kilovoltage or filtration thicknesses for a specific radiation quality.

The next script show how to use all the tools provided by the `XrayQualities` class.

```python
# Script to demonstrate the usage of XrayQualities class
from metpyx import XrayQualities

# Initialize an XrayQualities object
x = XrayQualities()

# List the X-ray radiation quality series
s = x.series
print(f'X-ray radiation quality series:\n{s}\n')

# List the L series radiation qualities
l = x.l_series
print(f'L series radiation qualities:\n{l}\n')

# List the N series radiation qualities
n = x.n_series
print(f'N series radiation qualities:\n{n}\n')

# List the W series radiation qualities
w = x.w_series
print(f'W series radiation qualities:\n{w}\n')

# List the H series radiation qualities
h = x.h_series
print(f'H series radiation qualities:\n{h}\n')

# Check if a series is an x-ray radiation quality series
print(f'Is L an x-ray radiation quality series?:\n{x.is_series('L')}\n')
print(f'Is X an x-ray radiation quality series?:\n{x.is_series('X')}\n')

# Check if a quality is an x-ray radiation quality
print(f'Is L10 an x-ray radiation quality?:\n{x.is_quality('L10')}\n')
print(f'Is L500 an x-ray radiation quality?:\n{x.is_quality('L500')}\n')

# Retrieve the radiation qualities of a radiation quality series
q = x.get_series_qualities('L')
print(f'L series radiation qualities:\n{q}\n')
print(f'X series radiation qualities:')
try:
    x.get_series_qualities('X')
except ValueError as e:
    print(f'{e}\n')

# Retrieve the series from a radiation quality
s = x.get_series('L10')
print(f'L10 quality belongs to series:\n{s}\n')
print(f'L500 quality belongs to series:')
try:
    x.get_series('L500')
except ValueError as e:
    print(f'{e}\n')

# Retrieve the peak kilovoltage from a radiation quality
kvp = x.get_peak_kilovoltage('L10')
print(f'Peak kilovoltage for L10 quality is:\n{kvp} kV\n')
print(f'Peak kilovoltage for L500 quality is:')
try:
    x.get_peak_kilovoltage('L500')
except ValueError as e:
    print(f'{e}\n')

# Retrieve the filtration thickness for a radiation quality
f = x.get_filtration_thickness('L10')
print(f'Filtration thickness for L10 quality is:\n{kvp}\n')
print(f'Filtration thickness for L500 quality is:')
try:
    x.get_filtration_thickness('L500')
except ValueError as e:
    print(f'{e}\n')
```

The script output is:

```
X-ray radiation quality series:
['L', 'N', 'W', 'H']

L series radiation qualities:
['L10', 'L20', 'L30', 'L35', 'L55', 'L70', 'L100', 'L125', 'L170', 'L210', 'L240']

N series radiation qualities:
['N10', 'N15', 'N20', 'N25', 'N30', 'N40', 'N60', 'N80', 'N100', 'N120', 'N150', 'N200', 'N250', 'N300', 'N350', 'N400']

W series radiation qualities:
['W30', 'W40', 'W60', 'W80', 'W110', 'W150', 'W200', 'W250', 'W300']

H series radiation qualities:
['H10', 'H20', 'H30', 'H40', 'H60', 'H80', 'H100', 'H150', 'H200', 'H250', 'H280', 'H300', 'H350', 'H400']

Is L an x-ray radiation quality series?:
True

Is X an x-ray radiation quality series?:
False

Is L10 an x-ray radiation quality?:
True

Is L500 an x-ray radiation quality?:
False

L series radiation qualities:
['L10', 'L20', 'L30', 'L35', 'L55', 'L70', 'L100', 'L125', 'L170', 'L210', 'L240']

X series radiation qualities:
X is not an x-ray radiation quality series.

L10 quality belongs to series:
L

L500 quality belongs to series:
L500 is not an x-ray radiation quality.

Peak kilovoltage for L10 quality is:
10 kV

Peak kilovoltage for L500 quality is:
L500 is not an x-ray radiation quality.

Filtration thickness for L10 quality is:
10

Filtration thickness for L500 quality is:
L500 is not an x-ray radiation quality.
```

### Managing x-ray operational quantities

The tool that **MetPyX** provides to manage x-ray operational quantities is the **XrayQuantities** class.
With **XrayQuantities** class you can:
- List the operational quantities for x-rays.
- Check if a quantity is an operational quantity for x-rays.
- Retrieve the irradiation angles for an operational quantity.

The next script show how to use all the tools provided by the `XrayQuantities` class.

```python
# Script to demonstrate the usage of XrayQuantities class
from metpyx import XrayQuantities

# Initialize an XrayQuantities object
x = XrayQuantities()

# List the operational quantities for x-rays
quantities = x.operational_quantities
print(f'Operational quantities for x-rays:\n{quantities}\n')

# Check if a quantity is an operational quantity for x-rays
print(f'Is H*(10) an operational quantity for x-rays?:\n{x.is_quantity('H*(10)')}\n')
print(f'Is H*(3) an operational quantity for x-rays?:\n{x.is_quantity('H*(3)')}\n')

# Retrieve the irradiation angles for an operational quantity
theta = x.get_irradiation_angles('Hp(0.07, slab)')
print(f'Irradiation angles for Hp(0.07, slab):\n{theta}\n')
print(f'Irradiation angles for H*(0.07):')
try:
    x.get_irradiation_angles('H*(0.07)')
except ValueError as e:
    print(f'{e}\n')
```

The script output is:

```
Operational quantities for x-rays:
['H_prime(0.07)', 'H_prime(3)', 'H*(10)', 'Hp(0.07, rod)', 'Hp(0.07, pillar)', 'Hp(0.07, slab)', 'Hp(3, cyl)', 'Hp(10, slab)']

Is H*(10) an operational quantity for x-rays?:
True

Is H*(3) an operational quantity for x-rays?:
False

Irradiation angles for Hp(0.07, slab):
[0, 15, 30, 45, 60, 75]

Irradiation angles for H*(0.07):
H*(0.07) is not an x-ray operational quantity.
```

## Future developments

If you have any suggestions for future versions of **MetPyX** please let us know (please check the 
[Contributing to MetPyX](#contributing-to-metpyx) section).

## How to get support?

If you need support, please check the **MetPyX** documentation at GitHub
([README](https://github.com/lmri-met/metpyx/blob/main/README.md)).

If you need further support, please send an e-mail to [Xandra Campo](mailto:xandra.campo@ciemat.es).

## Documentation

The official documentation of **MetPyX** is hosted on GitHub.
Check its [README](https://github.com/lmri-met/metpyx#README) file for a quick start guide.

## Contributors

**MetPyX** is developed and maintained by [Xandra Campo](https://github.com/xandratxan/).
It is one of the projects of the [Ionizing Radiation Metrology Laboratory (LMRI)](https://github.com/lmri-met/), 
which is the Spanish National Metrology Institute for ionizing radiation.

## License

**MetPyX** is distributed under the [GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/) License.

## Contributing to MetPyX

All contributions, bug reports, bug fixes, documentation improvements, enhancements, and ideas are welcome.
Please check the **MetPyX** [issues page](https://github.com/lmri-met/metpyx/issues) if you want to contribute.