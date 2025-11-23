# TODO: Add module docstring
# TODO: Add feature to do sensitivity analysis on simulated spectrum.
# TODO: Add feature to do uncertainty calculation on simulated spetrum using Monte Carlo.
import spekpy as sp

from metpyx.data import Qualities
from metpyx.spectrum import Spectrum


class SimulatedSpectrum(Spectrum):
    """Simulated X-ray spectrum produced via :mod:`spekpy`.

    Lightweight helper that constructs a :class:`Spectrum` by delegating to
    :mod:`spekpy` (``spekpy.Spek``). The class supports two mutually-
    exclusive initialization modes:

    - Quality-based: provide ``quality`` and (optionally) ``anode``; the
      class will look up voltage and filtration values via
      :class:`metpyx.data.Qualities` and use those to generate the spectrum.
    - Voltage-based: provide ``voltage`` (required in this mode)
      and optionally ``anode`` and ``filtration``; these values are
      forwarded to :mod:`spekpy` to produce the spectrum.

    The produced spectral arrays are passed to the base :class:`Spectrum`
    constructor for validation and storage. The resulting instance exposes
    the primary spectral attributes ``energy`` and ``fluence`` along with
    the generator parameters used to create the spectrum.

    Attributes
    ----------
    energy : numpy.ndarray
        1-D array of photon energies (inherited from :class:`Spectrum`).
    fluence : numpy.ndarray
        1-D array of fluence values corresponding to ``energy``.
    voltage : float or None
        Tube high voltage (kV) used to generate the spectrum.
    anode : float or None
        Anode parameter forwarded to :mod:`spekpy`.
    filtration : sequence or None
        Filtration descriptor as a sequence of (material, thickness) pairs.
        Thickness is in mm.
    quality : str or None
        Quality identifier if quality-based initialization is used.

    Notes
    -----
    - This class depends on :mod:`spekpy` for spectrum generation; ensure
      ``spekpy`` is installed in the runtime/test environment.
    - Any additional ``**kwargs`` passed to the constructor are forwarded
      to :class:`spekpy.Spek`.

    Examples
    --------
    Quality-based initialization::

        s = SimulatedSpectrum(quality='N30', anode=20)

    Voltage-based (explicit) initialization::

        s = SimulatedSpectrum(voltage=30, anode=20, filtration=[('Be', 1), ('Al', 4)])
    """

    def __init__(self, voltage=None, anode=None, filtration=None, quality=None, **kwargs):
        """Create a simulated spectrum.

        Parameters
        ----------
        voltage : float or None, optional
            Tube high voltage (kV). Required for explicit (voltage-based)
            initialization. Ignored when ``quality`` is provided.
        anode : float or None, optional
            Anode parameter forwarded to :mod:`spekpy`. Accepted in both
            initialization modes (when provided alongside ``quality`` it is
            forwarded directly to ``spekpy``).
        filtration : object or None, optional
            Filtration descriptor to apply (format expected by :mod:`spekpy`).
            In quality-based mode the filtration is obtained from
            :class:`Qualities` and the ``filtration`` argument must be ``None``.
        quality : str or None, optional
            Named quality identifier used to look up standard generator
            parameters (voltage/filtration) via :class:`metpyx.data.Qualities`.
            Mutually exclusive with explicit voltage/filtration inputs.
        **kwargs
            Extra keyword arguments are forwarded to :class:`spekpy.Spek`.

        Raises
        ------
        ValueError
            If ``quality`` is provided together with explicit
            ``voltage``/``filtration``, or if neither ``quality`` nor
            ``voltage`` is supplied.

        Notes
        -----
        - When ``quality`` is supplied the class queries :class:`Qualities`
          for the corresponding ``voltage`` and ``filtration`` values.
        - When ``voltage`` is supplied the constructor uses it directly and
          forwards ``anode`` and ``filtration`` (if present) to :mod:`spekpy`.
        - The method delegates validation of the produced arrays to the
          base :class:`Spectrum` constructor.
        """

        if quality is not None:
            # Quality-only initialization (voltage and filtration must be None)
            if voltage is not None or filtration is not None:
                raise ValueError(
                    f"Must initialize with either (`quality`, `anode`) or (`voltage`, `anode`, `filtration`).")
            _qualities = Qualities()
            self.quality = quality
            self.anode = anode
            self.voltage = _qualities.get_voltage(quality)
            self.filtration = _qualities.get_filtration(quality)

        elif voltage is not None:
            # Voltage initialization (quality must be None, and it is from the previous check)
            self.quality = None
            self.anode = anode
            self.voltage = voltage
            self.filtration = filtration

        else:
            # No valid initialization provided
            raise ValueError(f"Must initialize with either (`quality`, `anode`) or (`voltage`, `anode`, `filtration`).")

        # Generate spectrum using spekpy
        s = sp.Spek(self.voltage, self.anode, **kwargs)
        if self.filtration is not None:
            s.multi_filter(self.filtration)
        energy, fluence = s.get_spectrum()

        # Initialize base Spectrum class
        super().__init__(energy, fluence)
