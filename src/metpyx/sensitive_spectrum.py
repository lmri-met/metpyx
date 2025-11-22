"""src.sensitive_spectrum

Module to represent x-ray spectrum sensitivity analysis.

This module provides the SensitiveSpectrum class which models an x-ray
spectrum used for sensitivity/perturbation analysis. The class supports two
mutually-exclusive initialization patterns:

- Quality-only: provide a named reference quality via the ``quality``
  parameter (for example, 'N60').
- Explicit spectrum: provide numeric ``voltage`` (kV), ``anode`` angle
  (degrees) and ``filtration`` (an iterable of (material, thickness)
  pairs, e.g. [('Al', 4), ('Cu', 0.6)]).

The constructor also accepts metadata fields such as ``variable``,
``variation``, ``inherent`` and ``impurity`` which are stored on the
instance. The constructor enforces that exactly one initialization mode is
used: providing both quality and explicit spectrum parameters, or providing
none, will raise ValueError.

Notes:
- The module currently stores the provided ``filtration`` value without
  coercion; callers should supply an iterable of material/thickness pairs.
- Avoid placing executable examples at module import time; examples should
  live in tests or example scripts to prevent side effects on import.
"""

# Requirements of a module to represent an x-ray spectrum sensitivity analysis
#
# Summary:
# - The main goal of this module is to provide a class to represent an x-ray spectrum sensitivity analysis.
# - The class represent an x-ray spectrum that has been modified by varying one of its parameters by a certain percentage.
# - The class focuses on calculating the deviated spectrum characteristics and the effect of the variation in the spectrum characteristics with respect to the unvaried spectrum.
#
# About the class initialization:
# - The class is designed to represent any x-ray spectrum, specifying its high voltage, anode angle and filtration, just like SpekPy and USpekPy.
# - The class should also be able to represent reference field spectrum, i.e. x-ray qualities, using the MetPyX XrayQualities class.
#
# About the variation-related parameters:
# - The parameters that can be varied are high voltage, filtration thickness and filtration purity.
# - The class should be able to handle simultaneous variations in high voltage and filtration thickness.
#
# About the characterizing quantities:
# - The quantities that characterize the spectrum are: high voltage, anode angle and filtration.
# - The integral quantities that characterize the spectrum are: mean energy, HVL, air kerma, mean conversion coefficient.
#
# Miscellaneous:
# - This class subclasses a base class (SpekWrapper) that provides methods to calculate the integral quantities.
# - Possible names for the main class: SensitiveSpectrum, PerturbedSpectrum, DeviatedSpectrum, VariedSpectrum
from metpyx import XrayQualities


def dict_to_tuple_list(dictionary):
    """Convert a mapping to a list of (key, value) tuples.

    This utility converts a mapping (for example a dict) into an ordered list
    of (key, value) tuples. It preserves the iteration order of the provided
    mapping. The function is intentionally simple and behaves equivalently to
    list(dictionary.items()).

    Parameters
    ----------
    dictionary : Mapping
        The mapping to convert. Typically a dict where keys are materials or
        identifiers and values are numeric thicknesses or other properties.

    Returns
    -------
    list of tuple
        A list of (key, value) tuples in the order returned by iterating the
        mapping.

    Example
    -------
    >>> dict_to_tuple_list({'Al': 4, 'Cu': 0.6})
    [('Al', 4), ('Cu', 0.6)]
    """
    return [(i, j) for i, j in zip(dictionary.keys(), dictionary.values())]


class SensitiveSpectrum:
    """
    Represent an x-ray spectrum for sensitivity analysis.

    This class models an x-ray spectrum that can be specified in one of two
    mutually-exclusive ways:
      - Quality-only: provide a named reference quality (e.g. 'N60') via
        the ``quality`` parameter.
      - Explicit spectrum: provide numeric ``voltage`` (kV), ``anode`` angle
        (degrees) and ``filtration`` (an iterable of (material, thickness)
        pairs, e.g. [('Al', 4), ('Cu', 0.6)]).

    The constructor also accepts variation-related metadata fields
    (``variable``, ``variation``) and additional properties such as
    ``inherent`` and ``impurity`` which are stored as provided.

    Initialization rules (enforced by the constructor):
      - Providing both ``quality`` and any explicit spectrum parameter raises
        ValueError.
      - Providing no initialization parameters raises ValueError.
      - When using the explicit form, all three of ``voltage``, ``anode`` and
        ``filtration`` must be provided.

    Attributes (set after initialization):
      - quality: str or None
      - high_voltage: numeric or None (set from ``voltage``)
      - anode_angle: numeric or None (set from ``anode``)
      - filtration: iterable or None
      - variable, variation, inherent, impurity: stored as provided

    Notes:
      - ``filtration`` is expected to be an iterable of (material, thickness)
        pairs. The constructor currently stores the provided filtration value
        without additional coercion.
    """

    def __init__(self, voltage=None, anode=None, filtration=None, quality=None, variable=None, variation=0,
                 inherent=None, impurity=None):
        """
        Initialize a SensitiveSpectrum in one of three valid ways:
        - quality only: quality is provided (e.g. 'N60')
        - explicit spectrum: high_voltage, anode_angle and filtration provided
        - otherwise: raise ValueError
        """
        # Store variation-related fields unchanged
        self.variable = variable
        self.variation = variation
        self.inherent = inherent
        self.impurity = impurity

        # Check if any explicit parameter is provided
        explicit_params = (voltage is not None) or (anode is not None) or (filtration is not None)

        # Validate mutually exclusive initialization modes
        if quality is not None and explicit_params:
            raise ValueError(
                "SensitiveSpectrum initialization error: Provide either `quality` OR `high_voltage`/`anode_angle`/`filtration`, not both.")

        # Quality-only initialization
        if quality is not None:
            self.quality = quality
            _data = self._resolve_quality()
            self.voltage = _data.get("voltage")
            self.anode = None
            self.filtration = _data.get("filtration")
            return

        if explicit_params:
            # If any explicit parameter is provided we require all three
            if voltage is None or anode is None or filtration is None:
                raise ValueError(
                    "SensitiveSpectrum initialization error: When using explicit spectrum initialization you must provide `high_voltage`, `anode_angle` and `filtration`.")
            self.quality = None
            self.voltage = voltage
            self.anode = anode
            self.filtration = filtration
            return

        # No valid initialization provided
        raise ValueError(
            "SensitiveSpectrum initialization error: Must initialize with either `quality` or (`high_voltage`, `anode_angle`, `filtration`).")

    def _resolve_quality(self):
        """Resolve a named quality via MetPyX XrayQualities.

        Query MetPyX's XrayQualities for the named quality stored on the
        instance (self.quality) and return a small mapping describing the
        resolved spectrum parameters.

        Returns
        -------
        dict
            A dictionary with the following keys:
            - "voltage" (float or None): the nominal peak kilovoltage (kV)
              associated with the named quality, or None if unavailable.
            - "filtration" (list of (str, float) tuples or None): the
              filtration specification converted to a list of (material,
              thickness) tuples. The conversion is performed using
              :func:`dict_to_tuple_list` to normalize the value returned by
              XrayQualities.get_filtration_thickness(). If XrayQualities
              returns None, this value will also be None.

        Raises
        ------
        ValueError
            If ``self.quality`` is not a recognized quality name.

        Example
        -------
        >>> s = SensitiveSpectrum(quality='N60')
        >>> s._resolve_quality()
        {'voltage': 60.0, 'filtration': [('Al', 4)]}
        """
        x = XrayQualities()

        if not x.is_quality(self.quality):
            raise ValueError(f"SensitiveSpectrum error: Unknown quality '{self.quality}'.")

        voltage = x.get_peak_kilovoltage(self.quality)
        filtration = dict_to_tuple_list(x.get_filtration_thickness(self.quality))

        return {"voltage": voltage, "filtration": filtration}
