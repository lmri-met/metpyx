import numpy as np
from scipy.interpolate import Akima1DInterpolator
from spekpy import Spek

from metpyx.data import Qualities, Coefficients


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
        # Get distance from state and format filtration
        self.distance = self.state.spectrum_parameters.z
        self.spek_filtration = self._format_filtration_for_spek(self.total_filtration, self.distance)
        # Apply filtration
        self.multi_filter(self.spek_filtration)

    @staticmethod
    def _format_filtration_for_spek(filtration, distance):
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
        total_filtration = [[str(material), float(thickness)] for material, thickness in filtration.items()]
        # total_filtration_thickness = sum(filtration[1] for filtration in total_filtration)
        # air_thickness = distance * 10 - total_filtration_thickness # Convert distance from cm to mm
        air_thickness = distance * 10  # distance in cm, air thickness in mm
        air_filtration = ["Air", air_thickness]
        return total_filtration + [air_filtration]

    def get_hk_mean(self, quantity, angle):  # TODO
        # Get spectrum from SpekPy
        spectrum_data = self.get_spectrum(diff=False)
        # Get coefficients from source
        c = Coefficients()
        mu_tr_over_rho_data = c.get_mu_tr_over_rho_air()
        h_k_data = c.get_h_k(quantity=quantity, angle=angle)

        # Unpack arrays
        energies = np.array(spectrum_data[0])
        fluence = np.array(spectrum_data[1])
        mu_energies = np.array(mu_tr_over_rho_data[0])
        mu_values = np.array(mu_tr_over_rho_data[1])
        h_k_energies = np.array(h_k_data[0])
        h_k_values = np.array(h_k_data[1])

        # If there are zeros in mu_tr_over_rho_air or h_k values, remove them before interpolation
        if np.any(mu_values == 0):
            mask_mu = mu_values != 0
            filtered_mu_energies = mu_energies[mask_mu]
            filtered_mu_values = mu_values[mask_mu]
            print("Warning: Zeros found in mu_tr_over_rho_air values. They have been removed for interpolation.")
        else:
            filtered_mu_energies = mu_energies
            filtered_mu_values = mu_values

        if np.any(h_k_values == 0):
            mask_hk = h_k_values != 0
            filtered_hk_energies = h_k_energies[mask_hk]
            filtered_hk_values = h_k_values[mask_hk]
            print("Warning: Zeros found in h_k values. They have been removed for interpolation.")
        else:
            filtered_hk_energies = h_k_energies
            filtered_hk_values = h_k_values

        # Interpolate mu_tr_over_rho_air coefficients to spectrum energies
        interpolator = Akima1DInterpolator(x=np.log(filtered_mu_energies), y=np.log(filtered_mu_values))
        mu_tr_over_rho = np.exp(interpolator(np.log(energies)))

        # Interpolate h_k coefficients to spectrum energies
        interpolator = Akima1DInterpolator(x=np.log(filtered_hk_energies), y=np.log(filtered_hk_values))
        h_k = np.exp(interpolator(np.log(energies)))

        # Check for NaN values in interpolated results
        if np.any(np.isnan(mu_tr_over_rho)):
            print("Warning: NaN values found in interpolated mu_tr_over_rho_air.")
        if np.any(np.isnan(h_k)):
            print("Warning: NaN values found in interpolated h_k.")

        # Calculate mean conversion coefficient
        h_k_mean_numerator = np.nansum(fluence * energies * mu_tr_over_rho * h_k)
        h_k_mean_denominator = np.nansum(fluence * energies * mu_tr_over_rho)
        return h_k_mean_numerator/h_k_mean_denominator
