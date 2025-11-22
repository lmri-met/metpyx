"""metpyx.sensitive_spectrum

Utilities for working with reference x-ray qualities and a small
container type for sensitivity experiments.

This module provides side-effect-free helpers to resolve and normalize
reference x-ray qualities and a minimal container used to represent an
x-ray spectrum in sensitivity/perturbation analyses.

Functions
---------
resolve_quality
    Resolve a named reference quality into a dictionary with keys
    ``'voltage'`` and ``'filtration'``; filtration is normalized to a
    list of ``(material, thickness)`` tuples when available.

Classes
-------
SensitiveSpectrum
    Container for an x-ray spectrum specified either by a named quality
    or by explicit parameters (``voltage``, ``anode`` angle, and
    ``filtration``).

Notes
-----
- Filtration values returned by helpers are normalized to a list of
  ``(material, thickness)`` tuples. When an explicit ``filtration`` is
  provided to :class:`SensitiveSpectrum`, the value is stored as-is and
  not coerced by the constructor.

Examples
--------
>>> from metpyx.sensitive_spectrum import resolve_quality, SensitiveSpectrum
>>> resolve_quality('N60')['voltage']
60.0
>>> SensitiveSpectrum(quality='N60').filtration
[('Al', 4.0)]
"""

from metpyx import XrayQualities


def resolve_quality(quality):
    """Resolve a named quality via MetPyX XrayQualities.

    Parameters
    ----------
    quality : str
        Reference quality name (e.g. 'N60'). Validated with
        :class:`XrayQualities` (method ``is_quality``).

    Returns
    -------
    result : dict
        Dictionary containing:

        voltage : float or None
            Peak kilovoltage (kV) for the resolved quality, or ``None`` if
            not available from the qualities database.
        filtration : list of tuple or None
            Filtration as a list of ``(material, thickness)`` tuples, or
            ``None`` when no filtration information is present.

    Raises
    ------
    ValueError
        If ``quality`` is not a known quality according to
        :class:`XrayQualities`.
    """
    x = XrayQualities()

    if not x.is_quality(quality):
        raise ValueError(f"SensitiveSpectrum error: Unknown quality '{quality}'.")

    voltage = x.get_peak_kilovoltage(quality)
    filtration = list(x.get_filtration_thickness(quality).items())

    return {"voltage": voltage, "filtration": filtration}


class SensitiveSpectrum:
    """Container for an x-ray spectrum used in sensitivity analysis.

    The constructor supports one of two mutually-exclusive modes:

    1) Named-quality mode (pass ``quality``):
       The provided quality name (e.g. ``'N60'``) is resolved via
       :func:`resolve_quality`. The resolved ``voltage`` and normalized
       ``filtration`` populate the instance attributes; ``anode`` is set to
       ``None``. The original quality name is kept in ``quality``.

    2) Explicit-spectrum mode (provide ``voltage``, ``anode`` and
       ``filtration``):
       If any explicit parameter is supplied the constructor requires that
       all three (``voltage``, ``anode``, ``filtration``) are provided and
       non-``None``. In this mode ``quality`` is set to ``None`` and the
       provided ``filtration`` value is stored as given (no coercion).

    Parameters
    ----------
    voltage : float or None, optional
        Peak kilovoltage (kV) for an explicit spectrum. Default is ``None``.
    anode : float or None, optional
        Anode angle in degrees for an explicit spectrum. Default is ``None``.
    filtration : iterable of tuple or None, optional
        Filtration as an iterable of ``(material, thickness)`` pairs when
        supplying an explicit spectrum. When using a named quality,
        filtration is obtained from the qualities database and normalized to
        a list of tuples (or ``None`` if unavailable). Default is ``None``.
    quality : str or None, optional
        Named quality identifier (e.g. ``'N60'``). Mutually exclusive with
        explicit-spectrum parameters. Default is ``None``.
    variable : str or None, optional
        Optional metadata describing which parameter is being varied.
    variation : float, optional
        Optional metadata giving the variation magnitude. Default is ``0``.
    inherent : object, optional
        Additional optional metadata stored on the instance.
    impurity : object, optional
        Additional optional metadata stored on the instance.

    Raises
    ------
    ValueError
        If both ``quality`` and any explicit parameter are provided, if any
        explicit initialization parameter is missing, or if neither mode is
        satisfied. When resolving a named quality, the underlying
        :func:`resolve_quality` may also raise ``ValueError`` for unknown
        quality names.

    Attributes
    ----------
    quality : str or None
        Provided quality name (when using named-quality mode) or ``None``
        when explicit parameters were used.
    voltage : float or None
        Resolved or explicit peak kilovoltage (kV).
    anode : float or None
        Anode angle in degrees (explicit) or ``None`` when a named quality
        was used.
    filtration : list of tuple or any or None
        - When constructed from a named quality, filtration is normalized to
          a list of ``(material, thickness)`` tuples (or ``None`` if
          unavailable).
        - When constructed from explicit parameters, the provided
          ``filtration`` is stored as-is (no coercion by the constructor).
    variable, variation, inherent, impurity : as passed to constructor

    Examples
    --------
    >>> s = SensitiveSpectrum(quality='N60')
    >>> s.voltage
    60.0
    >>> s.filtration
    [('Al', 4.0)]
    """

    def __init__(self, voltage=None, anode=None, filtration=None, quality=None, variable=None, variation=0,
                 inherent=None, impurity=None):
        # Store variation-related fields unchanged
        self.variable = variable
        self.variation = variation
        self.inherent = inherent
        self.impurity = impurity

        # Check if any explicit parameter is provided
        explicit_params = (voltage is not None) or (anode is not None) or (filtration is not None)

        # Validate mutually exclusive initialization modes
        if quality is not None and explicit_params:
            raise ValueError(f"SensitiveSpectrum initialization error: "
                             f"Must initialize with either `quality` or (`voltage`, `anode`, `filtration`).")

        # Quality-only initialization
        if quality is not None:
            self.quality = quality
            _data = resolve_quality(quality)
            self.voltage = _data.get("voltage")
            self.anode = None
            self.filtration = _data.get("filtration")
            return

        if explicit_params:
            # If any explicit parameter is provided we require all three
            if voltage is None or anode is None or filtration is None:
                raise ValueError(f"SensitiveSpectrum initialization error: "
                                 f"When using explicit spectrum initialization you must provide "
                                 f"`high_voltage`, `anode_angle` and `filtration`.")
            self.quality = None
            self.voltage = voltage
            self.anode = anode
            self.filtration = filtration
            return

        # No valid initialization provided
        raise ValueError(f"SensitiveSpectrum initialization error: "
                         f"Must initialize with either `quality` or (`voltage`, `anode`, `filtration`).")
