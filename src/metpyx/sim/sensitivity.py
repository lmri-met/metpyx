from copy import deepcopy

from metpyx.data import Qualities, Densities
from metpyx.sim import Spectrum, format_filtration_for_spek


class QualitySensitivity:
    """Sensitivity analysis for an x-ray radiation quality.

    Performs a single-parameter sensitivity analysis by perturbing a specified
    quality parameter (tube voltage or filtration) and constructing nominal and
    perturbed :class:`Spectrum` instances for comparison.

    Parameters
    ----------
    quality : str
        Identifier of the radiation quality to analyse.
    parameter : {'tube_voltage', 'additional_filtration_thickness', 'additional_filtration_purity'}
        Parameter to perturb.
    deviation : float
        Percentage deviation to apply to the parameter.
    material : str, optional
        Material name used when perturbing filtration purity (required if
        ``parameter`` is ``'additional_filtration_purity'``).

    Attributes
    ----------
    nominal_params : dict
        Nominal spectrum parameters.
    perturbed_params : dict
        Perturbed spectrum parameters.
    nominal_spec, perturbed_spec : Spectrum
        Spectrum instances for nominal and perturbed parameters.
    distance : float
        Source-to-detector distance extracted from the Spectrum state.

    Notes
    -----
    This class delegates spectrum creation to :class:`Spectrum` and uses
    project data helpers to look up qualities and material densities.
    """
    SUPPORTED_PARAMETERS = {
        "tube_voltage",
        "additional_filtration_thickness",
        "additional_filtration_purity",
    }

    def __init__(self, quality, parameter, deviation, material=None, *args, **kwargs):
        """Initialize a sensitivity analysis for a radiation quality.

        This constructor loads nominal quality parameters, applies the requested
        perturbation to the selected parameter and creates Spectrum instances
        for both the nominal and perturbed configurations so downstream code
        can compare spectral changes.

        Parameters
        ----------
        quality : str
            Key identifying the radiation quality (used with :class:`Qualities`).
        parameter : {'tube_voltage', 'additional_filtration_thickness', 'additional_filtration_purity'}
            The single parameter to perturb.
        deviation : float
            Percentage deviation to apply to the parameter (e.g. 10.0 means +10%%,
            -5.0 means -5%%). For ``additional_filtration_purity`` this value is
            interpreted as the impurity percentage to introduce into the main
            additional filtration material.
        material : str, optional
            Required when ``parameter`` is ``'additional_filtration_purity'``;
            name of the impurity material to add.
        *args, **kwargs
            Forwarded to :class:`Spectrum` when constructing spectrum objects
            (e.g. options controlling spectrum generation).

        Raises
        ------
        ValueError
            If ``parameter`` is not supported or if ``material`` is required but
            not provided.

        Attributes
        ----------
        quality, parameter, deviation, material
            Input values stored on the instance.
        nominal_params : dict
            Nominal spectrum parameters (voltage, filtration mappings, etc.).
        perturbed_params : dict
            Parameters after applying the perturbation.
        nominal_spec, perturbed_spec : Spectrum
            Constructed Spectrum instances for nominal and perturbed cases.
        nominal_params['spek_filtration'], perturbed_params['spek_filtration'] : object
            Filtration formatted for the spek interface and added to the
            parameter dictionaries by this constructor.
        distance : float
            Source-to-detector distance extracted from the Spectrum state.

        Notes
        -----
        The method modifies copies of the quality parameters and does not
        mutate any global data. Any additional keyword arguments are passed
        directly to :class:`Spectrum` and must be compatible with its API.
        """
        # Check if the parameter is supported
        if parameter not in self.SUPPORTED_PARAMETERS:
            raise ValueError(f"Unsupported parameter: {parameter!r}")

        # Check if material is required and provided
        if parameter == "additional_filtration_purity" and material is None:
            raise ValueError("Material must be specified for 'additional_filtration_purity'")

        # Set attributes
        self.quality = quality
        self.parameter = parameter
        self.deviation = deviation
        self.material = material

        # Get nominal and perturbed parameters
        self.nominal_params = self._get_nominal_parameters()
        self.perturbed_params = self._get_perturbed_parameters()

        # Initialize Spectrum instances for nominal and perturbed parameters and extract distance and filtration information
        nominal = self._initialize_spectrum_instance(self.nominal_params, *args, **kwargs)
        perturbed = self._initialize_spectrum_instance(self.perturbed_params, *args, **kwargs)

        # Store the nominal and perturbed filtration parameters formatted for spekpy
        self.nominal_params['spek_filtration'] = nominal['spek_filtration']
        self.perturbed_params['spek_filtration'] = perturbed['spek_filtration']

        # Store the nominal and perturbed Spectrum instances
        self.nominal_spec = nominal['spek']
        self.perturbed_spec = perturbed['spek']

        # Store the distance (assuming it is the same for both nominal and perturbed parameters)
        self.distance = nominal['distance']

    @staticmethod
    def _initialize_spectrum_instance(params, *args, **kwargs):
        """Create and configure a Spectrum instance from parameters.

        This helper constructs a :class:`Spectrum` using the provided
        parameters, computes the source-to-detector distance from the
        spectrum state, formats the filtration for the spek interface and
        applies the multi-filter to the spectrum.

        Parameters
        ----------
        params : dict
            Dictionary with spectrum parameters. Expected keys include
            ``'tube_voltage'`` and ``'total_filtration'``.
        *args, **kwargs
            Additional arguments forwarded to the :class:`Spectrum` constructor.

        Returns
        -------
        dict
            A dictionary containing:
            - ``distance`` (float): source-to-detector distance extracted from
              the spectrum state.
            - ``spek`` (:class:`Spectrum`): the configured Spectrum instance.
            - ``spek_filtration`` (dict/list): filtration formatted for the
              spek interface.
        """
        # Initialize Spectrum objects for nominal and perturbed parameters
        spek = Spectrum(kvp=params['tube_voltage'], *args, **kwargs)

        # Get distance from state
        distance = spek.state.spectrum_parameters.z

        # Format filtration for spekpy
        spek_filtration = format_filtration_for_spek(params['total_filtration'], distance)

        # Add filtration to the Spectrum objects based on the nominal and perturbed parameters
        spek.multi_filter(spek_filtration)

        return {'distance': distance, 'spek': spek, 'spek_filtration': spek_filtration}

    def _get_nominal_parameters(self):
        """Retrieve nominal parameters for the specified quality.

        The method queries the project's data layer to obtain the default
        tube voltage and filtration values for the requested quality.

        Returns
        -------
        dict
            Dictionary with keys:
            - ``tube_voltage`` (float): nominal tube voltage in kVp.
            - ``inherent_filtration`` (dict): inherent filtration by material in mm.
            - ``additional_filtration`` (dict): additional filtration by material in mm.
            - ``total_filtration`` (dict): total filtration by material in mm.
        """
        q = Qualities()
        nominal = {
            "tube_voltage": q.get_voltage(self.quality),
            "inherent_filtration": q.get_filtration(self.quality, inherent=True),  # in mm
            "additional_filtration": q.get_filtration(self.quality, additional=True),  # in mm
            "total_filtration": q.get_filtration(self.quality),  # in mm
        }
        return nominal

    def _get_perturbed_parameters(self):
        """Compute perturbed parameters by applying the requested deviation.

        The method starts from the nominal parameters and applies the
        configured deviation to the selected parameter. Supported perturbations
        include tube voltage, additional filtration thickness, and additional
        filtration impurity.

        Returns
        -------
        dict
            A dictionary of parameters reflecting the perturbation. Keys mirror
            those returned by :meth:`_get_nominal_parameters`.
        """
        # Start with a copy of the nominal parameters
        perturbed = deepcopy(self.nominal_params.copy())

        if self.parameter == "tube_voltage":
            return self._perturb_tube_voltage(perturbed)

        if self.parameter == "additional_filtration_thickness":
            return self._perturb_additional_filtration_thickness(perturbed)

        if self.parameter == "additional_filtration_purity":
            return self._perturb_additional_filtration_purity(perturbed)

        return None # This line should never be reached due to the check in the constructor

    def _perturb_tube_voltage(self, perturbed):
        """Apply a percentage deviation to the tube high voltage.

        This method modifies the ``tube_voltage`` value in the provided
        parameters dictionary by scaling it according to ``self.deviation``.

        Parameters
        ----------
        perturbed : dict
            Copy of the nominal parameters to be modified.

        Returns
        -------
        dict
            The updated parameters dictionary with the perturbed ``tube_voltage``.
        """
        perturbed["tube_voltage"] *= (1 + self.deviation / 100)
        return perturbed

    def _perturb_additional_filtration_thickness(self, perturbed):
        """Apply a percentage deviation to additional filtration thickness.

        The deviation is applied to each material present in the
        ``additional_filtration`` mapping. The method recomputes ``total_filtration``
        by summing ``inherent_filtration`` and the modified ``additional_filtration``.

        Parameters
        ----------
        perturbed : dict
            Parameters dictionary that must contain ``inherent_filtration`` and
            ``additional_filtration`` mappings.

        Returns
        -------
        dict
            The updated parameters dictionary with a recomputed
            ``total_filtration`` reflecting the applied deviation.
        """
        # Get the nominal inherent and additional filtration
        inherent = perturbed["inherent_filtration"]

        # Get the nominal additional filtration thickness
        additional = perturbed["additional_filtration"]

        # Apply deviation to nominal additional filtration thickness:
        # the deviation is applied to all materials in the additional filtration,
        # but not to the inherent filtration
        for material, thickness in additional.items():
            additional[material] = thickness * (1 + self.deviation / 100)

        # Get the total filtration by summing inherent and additional filtration
        total = dict(inherent)
        for material, thickness in additional.items():
            total[material] = total.get(material, 0.0) + thickness

        # Update the perturbed parameters with the new total filtration
        perturbed["total_filtration"] = total

        return perturbed

    def _perturb_additional_filtration_purity(self, perturbed):
        """Introduce an impurity into the additional filtration.

        The method finds the main material in ``additional_filtration`` (the
        material with the largest thickness) and computes the equivalent
        thickness of the impurity required to represent the configured
        impurity percentage (``self.deviation``). The impurity is then added
        as an extra thin layer to ``additional_filtration`` and ``total_filtration``
        is recomputed.

        Parameters
        ----------
        perturbed : dict
            Parameters dictionary that must contain ``inherent_filtration`` and
            ``additional_filtration`` mappings.

        Returns
        -------
        dict
            The updated parameters dictionary with the impurity added to
            ``additional_filtration`` and a recomputed ``total_filtration``.
        """

        # Get the nominal inherent and additional filtration
        inherent = perturbed["inherent_filtration"]

        # Get the nominal additional filtration thickness
        additional = perturbed["additional_filtration"]

        # Apply deviation to nominal additional filtration thickness:
        # The deviation is applied to the material with the maximum thickness in the additional filtration.
        # The impurity is added as a thin layer of extra filtration to the additional filtration.

        # Find the material that has the maximum thickness in the additional filtration
        main_material = max(additional, key=additional.get)
        # Get the percentage of impurity in the main material
        p_imp = self.deviation
        # Get the thickness of the main material in the additional filtration
        d_mat = additional[main_material]
        # Get the densities of the main material and impurity
        d = Densities()
        rho_mat = d.get_density(main_material)
        rho_imp = d.get_density(self.material)
        # Get the equivalent thickness of the impurity and the superficial densities of the main material and impurity
        d_imp, sigma_imp, sigma_mat = get_equivalent_filter(d_mat, p_imp, rho_mat, rho_imp)

        # Add the impurity as a thin layer of extra filtration to the additional filtration
        additional[self.material] = d_imp

        # Get the total filtration by summing inherent and additional filtration
        total = dict(inherent)
        for material, thickness in additional.items():
            total[material] = total.get(material, 0.0) + thickness

        # Update the perturbed parameters with the new total filtration
        perturbed["total_filtration"] = total

        return perturbed

    def get_emean_dev(self, **kwargs):
        # TODO: add numpy style docstring
        nominal = self.nominal_spec.get_emean(**kwargs)
        perturbed = self.perturbed_spec.get_emean(**kwargs)
        percentage = abs(perturbed - nominal) / nominal * 100
        return nominal, perturbed, percentage

    def get_kerma_dev(self, **kwargs):
        # TODO: add numpy style docstring
        nominal = self.nominal_spec.get_kerma(**kwargs)
        perturbed = self.perturbed_spec.get_kerma(**kwargs)
        percentage = abs(perturbed - nominal) / nominal * 100
        return nominal, perturbed, percentage

    def get_hvl1_dev(self, **kwargs):
        # TODO: add numpy style docstring
        nominal = self.nominal_spec.get_hvl1(**kwargs)
        perturbed = self.perturbed_spec.get_hvl1(**kwargs)
        percentage = abs(perturbed - nominal) / nominal * 100
        return nominal, perturbed, percentage

    def get_hvl2_dev(self, **kwargs):
        # TODO: add numpy style docstring
        nominal = self.nominal_spec.get_hvl2(**kwargs)
        perturbed = self.perturbed_spec.get_hvl2(**kwargs)
        percentage = abs(perturbed - nominal) / nominal * 100
        return nominal, perturbed, percentage

    def get_hk_mean_dev(self, *args, **kwargs):
        # TODO: add numpy style docstring
        nominal = self.nominal_spec.get_hk_mean(*args, **kwargs)
        perturbed = self.perturbed_spec.get_hk_mean(*args, **kwargs)
        percentage = abs(perturbed - nominal) / nominal * 100
        return nominal, perturbed, percentage

    def get_dose_equivalent_dev(self, *args, **kwargs):
        # TODO: add numpy style docstring
        nominal = self.nominal_spec.get_dose_equivalent(*args, **kwargs)
        perturbed = self.perturbed_spec.get_dose_equivalent(*args, **kwargs)
        percentage = abs(perturbed - nominal) / nominal * 100
        return nominal, perturbed, percentage


def get_equivalent_filter(d_mat, p_imp, rho_mat, rho_imp):
    """
    Calculates the equivalent thickness and superficial densities of a composite X-ray filter
    composed of a base material and an impurity.

    This function estimates how much of the impurity material is needed to maintain the same
    attenuation characteristics as a pure filter of the base material, based on their densities
    and the impurity percentage.

    Parameters
    ----------
    d_mat : float
        Thickness of the base filter material in millimeters (mm).
    p_imp : float
        Percentage of impurity in the filter material (0–100).
    rho_mat : float
        Density of the base filter material in g/cm³.
    rho_imp : float
        Density of the impurity material in g/cm³.

    Returns
    -------
    tuple
        A tuple containing:
        - d_imp (float): Equivalent thickness of the impurity material in mm.
        - sigma_imp (float): Superficial density of the impurity in mg/cm².
        - sigma_mat (float): Superficial density of the base material in mg/cm².

    Notes
    -----
    The equivalent thickness of the impurity (`d_imp`) is calculated to ensure that the
    mass per unit area (superficial density) of the impurity matches its proportion in the
    composite filter. The formula used is:

    d_imp = d_mat * (ρ_mat * f_imp) / (ρ_imp * f_mat)

    where:
    - f_imp = p_imp / 100 is the fractional impurity content,
    - f_mat = 1 - f_imp is the fractional base material content,
    - ρ_mat and ρ_imp are the densities of the base and impurity materials, respectively.

    The superficial densities (σ) are calculated as:

    σ = ρ × d / 10

    to convert from g/cm² to mg/cm².
    The function assumes a homogeneous mixture of the base and impurity materials.
    """
    # Fractional impurity content
    f_imp = p_imp / 100
    # Fractional base material content
    f_mat = 1 - f_imp
    # Equivalent thickness of the impurity (mm)
    d_imp = d_mat * (rho_mat * f_imp) / (rho_imp * f_mat)
    # Superficial densities of the impurity (mg/cm²)
    sigma_imp = rho_imp * d_imp / 10
    # Superficial densities of the impurity (mg/cm²)
    sigma_mat = rho_mat * d_mat / 10
    return d_imp, sigma_imp, sigma_mat
