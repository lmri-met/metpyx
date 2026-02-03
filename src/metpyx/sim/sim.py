from spekpy import Spek

from metpyx.data import Qualities


class Quality(Spek):
    """
    Spek subclass initialized from a named X-ray quality.

    This class constructs a spekpy.Spek spectrum using standard named
    X-ray qualities (for example, ``'N60'``). It looks up the nominal
    tube voltage and the total filtration for the named quality from the
    package's `Qualities` registry, initializes the parent ``Spek``
    object with that voltage, and applies the corresponding multifilter
    to the spectrum.

    Parameters
    ----------
    quality : str
        Quality name (e.g. ``'N60'``).
    **spek_kwargs : Any
        Additional keyword arguments forwarded to :class:`spekpy.Spek`.

    Attributes
    ----------
    quality : str
        The provided quality name.
    voltage : float
        The nominal tube voltage (kVp) looked up from :class:`Qualities`.
    total_filtration : dict
        Mapping of filter material to thickness (e.g. ``{"Al": 4, "Cu": 0.6}``).

    Raises
    ------
    KeyError
        If the provided quality name is not found in the :class:`Qualities`
        registry.

    Notes
    -----
    The class intentionally subclasses :class:`spekpy.Spek` so that
    all ``Spek`` methods (for example ``get_emean``, ``get_kerma``, and
    ``get_hvl1``) are available on :class:`Quality` instances.
    """

    def __init__(self, quality, **spek_kwargs):
        """
        Create a :class:`Quality`-backed spectrum.

        Parameters
        ----------
        quality : str
            Named X-ray quality (see class docstring).
        **spek_kwargs : Any
            Forwarded to :class:`spekpy.Spek` during initialization.

        Notes
        -----
        After the parent :class:`spekpy.Spek` is initialized with the
        looked-up ``kvp``, the quality's total filtration is formatted
        and applied using :meth:`spekpy.Spek.multi_filter`.
        """
        # Store quality name
        self.quality = quality

        # Get voltage and filtration for quality
        q = Qualities()
        self.voltage = q.get_voltage(quality)
        self.total_filtration = q.get_filtration(quality)

        # Initialize parent Spek class
        super().__init__(kvp=self.voltage, **spek_kwargs)

        # Format and apply total filtration (standard qualities always have filtration)
        formatted = self._format_filtration_for_spek(self.total_filtration)
        self.multi_filter(formatted)

    @staticmethod
    def _format_filtration_for_spek(filtration):
        """
        Format total filtration for :meth:`spekpy.Spek.multi_filter`.

        The :class:`Qualities` registry provides filtration as a mapping
        from material name to thickness. :func:`spekpy.Spek.multi_filter`
        expects a sequence of ``[material, thickness]`` pairs where the
        material is a string and the thickness is a floating-point value.

        Parameters
        ----------
        filtration : Mapping
            Mapping of material name to thickness (int/float), for
            example ``{"Al": 4, "Cu": 0.6}``.

        Returns
        -------
        list
            A list of ``[material, thickness]`` pairs suitable for
            passing to :meth:`spekpy.Spek.multi_filter`, for example
            ``[["Al", 4.0], ["Cu", 0.6]]``.

        Notes
        -----
        This is an internal helper and is intentionally prefixed with
        a single leading underscore. It does not validate material names
        beyond converting them to strings and casting thicknesses to
        :class:`float`.
        """
        return [[str(material), float(thickness)] for material, thickness in filtration.items()]
