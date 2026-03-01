import warnings

import numpy as np
from scipy.interpolate import Akima1DInterpolator
from spekpy import Spek

from metpyx.data import Coefficients
from metpyx.data import Qualities


class Spectrum(Spek):
    """
    Spek subclass providing dose-related utilities.

    Represents an X-ray spectrum built on top of `spekpy.Spek` and provides utilities
    to compute the mean air-kerma-to-dose conversion coefficient and the dose
    equivalent for a given operational quantity and irradiation angle.

    Parameters
    ----------
    **kwargs : dict
        Keyword arguments forwarded to the `spekpy.Spek` constructor.
    """

    def __init__(self, **kwargs):
        """Initialize the Spectrum.

        Parameters
        ----------
        **spek_kwargs : dict
            Keyword arguments forwarded to the parent :class:`spekpy.Spek`.
        """
        super().__init__(**kwargs)

    def get_hk_mean(self, quantity, angle, mu_tr_over_rho_source=None, h_k_source=None):
        """Compute mean air kerma to dose conversion coefficient (Sv/Gy).

        Parameters
        ----------
        quantity : str
            Operational quantity name.
        angle : float
            Irradiation angle (degrees).
        mu_tr_over_rho_source : str, optional
            Source name for mass energy transfer coefficients of air.
            If None, default source is used ("pene_2018").
            Possible sources include "pene_2018".
            See `metpyx.data.Coefficients`.
        h_k_source : str, optional
            Source name for air-kerma-to-dose conversion coefficients.
            If None, default source is used ("cmi_2025).
            Possible sources include "cmi_2025".
            See `metpyx.data.Coefficients`.

        Returns
        -------
        float
            Mean air kerma to dose conversion coefficient (Sv/Gy).

        Notes
        -----
        Expected units are keV for energies, 1/cm² for fluence, cm²/g for mass energy transfer coefficients of air,
        Sv/Gy for air-kerma-to-dose conversion coefficients.
        Mean air kerma to dose conversion coefficient is calculated as weighted sum:
        h_K_mean = sum(Φ(E) * E * (μ_tr/ρ)_air(E) * h_k(E)) / sum(Φ(E) * E * (μ_tr/ρ)_air(E))
        Coefficient data are obtained from `metpyx.data.Coefficients`.
        Interpolation is performed on a log-log scale using an Akima interpolator.
        Zero-valued coefficients are removed before interpolation.
        Interpolating outside the coefficient energy ranges can produce `NaN` values;
        such `NaN` results currently trigger a warnings and
        np.nansum() is used to ignore any NaN values in the summation.
        """

        # Get spectrum from SpekPy
        spectrum_data = self.get_spectrum(diff=False)
        # Get coefficients from source
        c = Coefficients()
        mu_tr_over_rho_data = c.get_mu_tr_over_rho_air(source=mu_tr_over_rho_source)
        h_k_data = c.get_h_k(quantity, angle, source=h_k_source)

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
            warnings.warn("Zeros found in mu_tr_over_rho_air values; removed for interpolation.")
        else:
            filtered_mu_energies = mu_energies
            filtered_mu_values = mu_values

        if np.any(h_k_values == 0):
            mask_hk = h_k_values != 0
            filtered_hk_energies = h_k_energies[mask_hk]
            filtered_hk_values = h_k_values[mask_hk]
            warnings.warn("Zeros found in h_k values; removed for interpolation.")
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
            warnings.warn("NaN values found in interpolated mu_tr_over_rho_air.")
        if np.any(np.isnan(h_k)):
            warnings.warn("NaN values found in interpolated h_k.")

        # Calculate mean conversion coefficient
        h_k_mean_numerator = np.nansum(fluence * energies * mu_tr_over_rho * h_k)
        h_k_mean_denominator = np.nansum(fluence * energies * mu_tr_over_rho)
        return h_k_mean_numerator / h_k_mean_denominator

    def get_dose_equivalent(self, quantity, angle):
        """Compute dose equivalent for a given operational quantity and irradiation angle (uSv).

        Parameters
        ----------
        quantity : str
            Operational quantity name.
        angle : float
            Irradiation angle (degrees).

        Returns
        -------
        float
            Dose equivalent in microSievert (uSv).

        Notes
        -----
        Expected units are uGy for air kerma and Sv/Gy for mean air-kerma-to-dose conversion coefficient.
        Dose equivalent is calculated as the product of air kerma and the mean air-kerma-to-dose conversion coefficient.
        """

        h_k_mean = self.get_hk_mean(quantity=quantity, angle=angle)  # Sv/Gy
        kerma = self.get_kerma()  # uGy
        return kerma * h_k_mean  # uGy * Sv/Gy = uSv


class Quality(Spectrum):
    """
    Spectrum subclass initialized from a named X-ray quality.

    This class constructs a ``metpyx.sim.Spectrum`` using standard named
    X-ray qualities (for example, ``'N60'``). It looks up the nominal
    tube voltage and the total filtration for the named quality from the
    package's `Qualities` registry, initializes the parent ``Spectrum``
    object with that voltage, formats the filtration for ``spekpy``,
    and applies the corresponding multifilter to the spectrum.

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
        The nominal tube voltage (kVp) for the provided quality.
    total_filtration : dict
        Mapping of filter material to thickness (mm) for the provided quality (e.g. ``{"Al": 4, "Cu": 0.6}``).
    spek_filtration : list
        Formatted filtration list (mm) suitable for passing to :meth:`spekpy.Spek.multi_filter (e.g. ``[["Al", 4.0], ["Cu", 0.6]]``), adding an "Air" filter based on the distance from the source to the point of interest.
    distance : float
        Source-to-detector distance taken from (cm).
    """

    def __init__(self, quality, **kwargs):
        """
        Initialize the Quality instance.

        Parameters
        ----------
        quality : str
            The provided quality name.
       **spek_kwargs : Any
            Additional keyword arguments forwarded to :class:`spekpy.Spek`.
        """
        # Store quality name
        self.quality = quality

        # Get voltage and filtration for quality
        q = Qualities()
        self.voltage = q.get_voltage(quality)
        self.total_filtration = q.get_filtration(quality)

        # Initialize parent Spek class
        super().__init__(kvp=self.voltage, **kwargs)

        # Get distance from state and format filtration
        self.distance = self.state.spectrum_parameters.z
        self.spek_filtration = format_filtration_for_spek(self.total_filtration, self.distance)

        # Apply filtration
        self.multi_filter(self.spek_filtration)


def format_filtration_for_spek(filtration, distance):
    """
    Format total filtration for :meth:`spekpy.Spek.multi_filter`.

    Parameters
    ----------
    filtration : Mapping
        Mapping of material name to thickness (mm), for example ``{"Al": 4, "Cu": 0.6}``.

    Returns
    -------
    list
        A list of ``[material, thickness]`` pairs suitable for passing to `spekpy.Spek.multi_filter`,
        for example ``[["Al", 4.0], ["Cu", 0.6]]``.
    """
    total_filtration = [[str(material), float(thickness)] for material, thickness in filtration.items()]
    # total_filtration_thickness = sum(filtration[1] for filtration in total_filtration)
    # air_thickness = distance * 10 - total_filtration_thickness # Convert distance from cm to mm
    air_thickness = distance * 10  # distance in cm, air thickness in mm
    air_filtration = ["Air", air_thickness]
    return total_filtration + [air_filtration]
