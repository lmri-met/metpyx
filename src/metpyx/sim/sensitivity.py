import warnings
from copy import deepcopy

import numpy as np
import statsmodels.api as sm
from matplotlib import pyplot as plt

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
        Identifier of the radiation quality to analyze.
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

    def __init__(self, quality, parameter, deviation, material=None, **kwargs):
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
        **kwargs
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
        nominal = self._initialize_spectrum_instance(self.nominal_params, **kwargs)
        perturbed = self._initialize_spectrum_instance(self.perturbed_params, **kwargs)

        # Store the nominal and perturbed filtration parameters formatted for spekpy
        self.nominal_params['spek_filtration'] = nominal['spek_filtration']
        self.perturbed_params['spek_filtration'] = perturbed['spek_filtration']

        # Store the nominal and perturbed Spectrum instances
        self.nominal_spec = nominal['spek']
        self.perturbed_spec = perturbed['spek']

        # Store the distance (assuming it is the same for both nominal and perturbed parameters)
        self.distance = nominal['distance']

    @staticmethod
    def _initialize_spectrum_instance(params, **kwargs):
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
        spek = Spectrum(kvp=params['tube_voltage'], **kwargs)

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

        return None  # This line should never be reached due to the check in the constructor

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
        percentage = (perturbed - nominal) / nominal * 100
        return nominal, perturbed, percentage

    def get_kerma_dev(self, **kwargs):
        # TODO: add numpy style docstring
        nominal = self.nominal_spec.get_kerma(**kwargs)
        perturbed = self.perturbed_spec.get_kerma(**kwargs)
        percentage = (perturbed - nominal) / nominal * 100
        return nominal, perturbed, percentage

    def get_hvl1_dev(self, **kwargs):
        # TODO: add numpy style docstring
        nominal = self.nominal_spec.get_hvl1(**kwargs)
        perturbed = self.perturbed_spec.get_hvl1(**kwargs)
        percentage = (perturbed - nominal) / nominal * 100
        return nominal, perturbed, percentage

    def get_hvl2_dev(self, **kwargs):
        # TODO: add numpy style docstring
        nominal = self.nominal_spec.get_hvl2(**kwargs)
        perturbed = self.perturbed_spec.get_hvl2(**kwargs)
        percentage = (perturbed - nominal) / nominal * 100
        return nominal, perturbed, percentage

    def get_hk_mean_dev(self, *args, **kwargs):
        # TODO: add numpy style docstring
        nominal = self.nominal_spec.get_hk_mean(*args, **kwargs)
        perturbed = self.perturbed_spec.get_hk_mean(*args, **kwargs)
        percentage = (perturbed - nominal) / nominal * 100
        return nominal, perturbed, percentage

    def get_dose_equivalent_dev(self, *args, **kwargs):
        # TODO: add numpy style docstring
        nominal = self.nominal_spec.get_dose_equivalent(*args, **kwargs)
        perturbed = self.perturbed_spec.get_dose_equivalent(*args, **kwargs)
        percentage = (perturbed - nominal) / nominal * 100
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


class QualityRequirements:
    """
    Compute linear relationship between a parameter deviation (e.g. tube voltage)
    and the mean air-kerma-to-dose conversion coefficient deviation, using
    metpyx.sim.QualitySensitivity for the underlying simulations.

    Parameters
    ----------
    quality : str
        Radiation quality identifier (e.g. ``"N60"``).
    parameter : str
        The single parameter to evaluate (e.g. ``"tube_voltage"``).
        Options are 'tube_voltage', 'additional_filtration_thickness' or 'additional_filtration_purity'.
    quantity : str
        Operational quantity (e.g. ``"h_star_10"``).
    angle : float or int
        Irradiation angle in degrees.
    deviations : array-like, optional
        Sequence of parameter deviations (percent). If ``None``, defaults to
        ``np.linspace(0, 10, 11)``.
    material : str, optional
        Required when ``parameter`` is ``'additional_filtration_purity'``;
        name of the impurity material to add. Default is ``None``.
    target : float, optional
        Target mean conversion coefficient deviation (percent) used to compute the
        requirement limit. Default is ``2``.
    r_squared : float, optional
        Minimum R² threshold to accept linearity. Default is ``0.7``.
    p_value : float, optional
        Maximum p-value threshold to accept linearity and
        minimum p-value threshold to accept intercept as statistically zero.
        Default is ``0.05``.
    atol : float, optional
        Absolute tolerance used to decide whether intercept is practically zero.
        Default is ``1.0`` (percentage point).
    kwargs : dict, optional
        Additional keyword arguments forwarded to ``QualitySensitivity``.

    Attributes
    ----------
    qs_instances : list of QualitySensitivity or None
        List of ``QualitySensitivity`` instances created for each parameter deviation.
    mean_hk : dict or None
        Dictionary with nominal (Sv/Gy), deviated (Sv/Gy), and deviation (%) values of mean conversion coefficient.
        Keys are ``'nominal'``, ``'deviated'``, ``'deviation'``.
    x, y : ndarray or None
        Independent and dependent variables used for the fit:
        parameter deviations and mean conversion coefficient deviations, respectively.
    sm_results : statsmodels RegressionResults or None
        Fitted OLS results.
    slope, intercept : tuple or None
        Tuples with (value, standard error, percent standard error) for slope and intercept.
    accept_linear : bool or None
        Whether the linear model is plausible based on the configured criteria (slope p-value and R²).
    accept_intercept_zero : bool or None
        Whether the intercept is statistically and practically consistent with zero based on the configured criteria
        (intercept p-value, 95% confidence interval, and absolute tolerance).
    requirement : tuple or None
        Computed parameter deviation limit in percent as (value, standard error, percent standard error).
    extrapolation_needed : bool or None
        Whether the computed limit is outside the supplied deviation range.
    """

    def __init__(self, quality, parameter, quantity, angle, deviations=None, material=None, target=2, r_squared=0.7,
                 p_value=0.05, atol=1.0, **kwargs):
        # Store arguments as attributes
        self.quality = quality
        self.parameter = parameter
        self.quantity = quantity
        self.angle = angle
        self.deviations = (np.asarray(deviations) if deviations is not None else np.linspace(0, 10, 11))
        self.material = material
        self.target = target
        self.r_squared = r_squared
        self.p_value = p_value
        self.atol = atol
        self.kwargs = {**kwargs}
        # Storage attributes for results
        self.qs_instances = None
        self.mean_hk = None
        self.x = None
        self.y = None
        self.sm_results = None
        self.slope = None
        self.intercept = None
        self.accept_linear = None
        self.accept_intercept_zero = None
        self.requirement = None
        self.extrapolation_needed = None

    def compute_deviations(self):
        """
        Compute the deviation in mean air-kerma-to-dose conversion coefficient for the deviations provided.

        The method calls ``QualitySensitivity`` for each parameter deviation and build the dependent
        variable array of mean conversion coefficient deviations.
        The method stores the independent variable (parameter deviations) and dependent variable (mean conversion
        coefficient deviations) as attributes for later use in fitting the model.
        The method also stores the nominal, deviated, and deviation values of the mean conversion coefficient in as
        an attribute for later inspection.
        The method checks the sample size and warns if the sample size is small (e.g. <= 3).

        Returns
        -------
        x : ndarray
            Independent variable array (parameter deviations in percent).
        y : ndarray
            Dependent variable array (mean conversion coefficient deviations in percent).
        """
        # Initialize a dictionary to store nominal, deviated, and deviation values for each parameter deviation
        values = {'nominal': [], 'deviated': [], 'deviation': []}
        qs_instances = []

        # Compute the mean conversion coefficient deviations for each parameter deviation
        for d in self.deviations:
            q = QualitySensitivity(self.quality, self.parameter, d, self.material, **self.kwargs)
            out = q.get_hk_mean_dev(self.quantity, self.angle)
            qs_instances.append(q)
            values['nominal'].append(out[0])
            values['deviated'].append(out[1])
            values['deviation'].append(out[2])

        # Store the results in attributes for later use
        self.qs_instances = qs_instances
        self.mean_hk = values
        self.x = np.asarray(self.deviations, dtype=float)
        self.y = np.asarray(values['deviation'], dtype=float)

        # Check sample size and warn about limitations if small
        self.check_sample_size()

        return self.x, self.y

    def fit_model(self):
        """
        Fit a linear model between the mean conversion coefficient deviation and the parameter deviation.

        The method computes the mean-air kerma-to-dose conversion coefficient deviations
        if they have not been computed yet.
        The method uses an ordinary least squares (OLS) linear model from ``statsmodels.api.OLS``
        to fit the model in the form y = intercept + slope * x.
        The method checks the linearity of the relationship and
        whether the intercept is significantly different from zero.
        The method stores the fitted model results and the slope and intercept estimates
        with their standard errors and percent standard errors as attributes.

        Returns
        -------
        slope : tuple
            ``(estimate, standard_error, percent_standard_error)`` for the slope.
        intercept : tuple
            ``(estimate, standard_error, percent_standard_error)`` for the intercept.
        """
        # Check if deviations have been computed, if not compute them
        if self.x is None or self.y is None:
            self.compute_deviations()

        # Fit the linear model using statsmodels OLS
        X = sm.add_constant(self.x)
        model = sm.OLS(self.y, X)
        res = model.fit()

        # Extract parameters and standard errors
        intercept, slope = res.params
        intercept_se, slope_se = res.bse

        # Store the results in attributes for later use
        self.sm_results = res
        self.slope = (slope, slope_se, slope_se / slope * 100)
        self.intercept = (intercept, intercept_se, intercept_se / intercept * 100)

        # Check linearity of the model and intercept being not significantly different from zero
        self.check_linearity()
        self.check_intercept()

        return self.slope, self.intercept

    def get_requirement(self):
        """
        Compute the parameter deviation limit that corresponds to the configured
        ``target`` mean conversion coefficient deviation using the fitted linear model.

        The method fits the model if it has not been fitted yet.
        The method stores the computed requirement limit and its uncertainty as an attribute for later use.
        The method checks if the computed limit is within the range of the provided deviations,
        and warns if extrapolation is needed to meet the target requirement.
        The method warns if both negative and positive deviations are provided,
        as the limit for the requirement may be different for positive and negative values of the target requirement.

        Returns
        -------
        requirement : tuple
            ``(limit, limit_se, limit_percent_se)`` where ``limit`` is the required
            parameter deviation (percent), ``limit_se`` its standard error, and
            ``limit_percent_se`` the relative standard error in percent.

        Notes
        -----
        If the slope is (approximately) zero, ``(None, None, None)`` is returned
        and a warning is issued.
        """

        # Check if the model has been fitted, if not fit it
        if self.sm_results is None:
            self.fit_model()

        # Check that the slope is not approximately zero to avoid division by zero when calculating the requirement
        if np.isclose(self.slope[0], 0.0):
            # Initialize requirement value and standard error to None in case the slope is approximately zero
            warnings.warn("Slope approximately zero: cannot compute finite requirement.")
            limit, limit_se, limit_percent_se = None, None, None
            self.requirement = (limit, limit_se, limit_percent_se)
        else:
            # Warn if both negative and positive deviations are provided, as the limit for the requirement may be
            # different for positive and negative values of the target requirement
            has_negative_and_positive = (self.x < 0).any() and (self.x > 0).any()
            if has_negative_and_positive:
                warnings.warn("Negative and positive deviations provided: "
                              "consider evaluating the positive and negative value of the target requirement.")

            # Compute requirement for configured target and fitted model and
            # propagate the uncertainty in the slope and intercept

            # Extract the slope and intercept estimates and their standard errors from the fitted model
            target = self.target
            slope, slope_se = self.slope[0], self.slope[1]
            intercept, intercept_se = self.intercept[0], self.intercept[1]

            # Compute the requirement limit
            limit = (target - intercept) / slope

            # Calculate the partial derivatives
            df_dslope = - (target - intercept) / slope ** 2
            df_dintercept = -1 / slope

            # Calculate the variances of the slope and intercept
            var_slope = slope_se ** 2
            var_intercept = intercept_se ** 2

            # Assuming slope and intercept are independent, the covariance is zero
            cov_slope_intercept = 0

            # Calculate the variance of the tube voltage deviation limit
            limit_var = (df_dslope ** 2 * var_slope) + (df_dintercept ** 2 * var_intercept) + (
                    2 * df_dslope * df_dintercept * cov_slope_intercept)

            # Calculate the standard error of the tube voltage deviation limit
            limit_se = np.sqrt(limit_var)

            # Calculate the percent standard error of the limit
            limit_percent_se = limit_se / limit * 100

            # Store the requirement in an attribute for later use
            self.requirement = (limit, limit_se, limit_percent_se)

            # Check if the limit is within the range of the deviations provided, and warn if extrapolation is needed to meet the target requirement
            self.check_extrapolation()

        return self.requirement

    def check_sample_size(self):
        """
        Check and warn if the sample size is too small (less or equal to 3).

        Raises
        ------
        RuntimeError
            If deviations have not been computed (``x`` or ``y`` is ``None``).
        """
        if self.x is None or self.y is None:
            raise RuntimeError("Deviations not computed: "
                               "please run `compute_deviations()` before calling `check_sample_size()`.")

        if self.x is not None and self.y is not None and self.x.size <= 3:
            warnings.warn("Small sample size (<=3). Statistical tests and confidence intervals may be unreliable.")

    def check_linearity(self):
        """
        Evaluate linearity of the model using slope p-value and R² and warn if linearity criteria are not met.

        The method checks if the model has been fitted, if not raises an error asking to fit the model first.
        The method checks the linearity of the model based on the configured criteria.
        The model is considered linear if the slope p-value is below the configured threshold and
        if R² is above the configured threshold.
        The method issues a warning if the linearity criteria are not met.
        The method stores the result of the linearity check in an attribute for later use.

        Returns
        -------
        accept_linear : bool
            ``True`` if the linear model is plausible based on the criteria, else ``False``.

        Raises
        ------
        RuntimeError
            If the model has not been fitted.
        """
        # Check if the model has been fitted, if not raise an error
        if self.sm_results is None:
            raise RuntimeError("Model not fitted: please run `fit_model()` before calling `check_linearity()`.")

        # Evaluate linearity criteria: slope p-value < threshold and R² > threshold
        slope_pvalue = self.sm_results.pvalues[1]
        r_squared = self.sm_results.rsquared
        self.accept_linear = (slope_pvalue < self.p_value) and (r_squared > self.r_squared)

        # Warn if linearity criteria are not met
        if not self.accept_linear:
            warnings.warn(f"The linear model may not be a good fit for the data."
                          f"Linearity criteria: slope p-value < {self.p_value} and R² > {self.r_squared}."
                          f"Found values: slope p-value = {slope_pvalue}, R² = {r_squared}.")
        return self.accept_linear

    def check_intercept(self):
        """
        Check whether the intercept is statistically and practically consistent with zero.

        The method checks if the model has been fitted, if not raises an error asking to fit the model first.
        The method checks if intercept is not significantly different from zero based on the configured criteria.
        Statistical criteria: intercept p-value > threshold and 95% confidence interval includes zero.
        Practical criteria: the fitted intercept is close to zero within the absolute tolerance configured.
        The method issues a warning if the intercept is significantly different from zero.
        The method stores the result of the intercept check in an attribute for later use.

        Returns
        -------
        accept_intercept_zero : bool
            ``True`` if both the statistical and practical criteria are met, else ``False``.

        Raises
        ------
        RuntimeError
            If the model has not been fitted.
        """
        # Check if the model has been fitted, if not raise an error
        if self.sm_results is None:
            raise RuntimeError("Model not fitted: please run `fit_model()` before calling `check_intercept()`.")

        # Evaluate if intercept is not significantly different from zero based on the configured criteria:
        # Statistical criteria: intercept p-value > threshold and 95% confidence interval includes zero.
        # Practical criteria: the fitted intercept is close to zero within the absolute tolerance configured.
        intercept_pvalue = self.sm_results.pvalues[0]
        intercept_ci = self.sm_results.conf_int(alpha=0.05)[0]
        intercept = self.sm_results.params[0]
        statistical = (intercept_pvalue > self.p_value) and (intercept_ci[0] < 0 < intercept_ci[1])
        practical = np.isclose(intercept, 0.0, atol=self.atol)
        self.accept_intercept_zero = statistical and practical

        # Warn if the intercept is significantly different from zero
        if not self.accept_intercept_zero:
            warnings.warn(f"The intercept of the linear fit is significantly different from zero."
                          f"Intercept criteria:"
                          f"Statistical: intercept p-value > {self.p_value} and 95% CI includes zero"
                          f"Practical: absolute difference below {self.atol} percentage point"
                          f"Found values: "
                          f"intercept p-value = {intercept_pvalue}, 95% CI = [{intercept_ci[0]}, {intercept_ci[1]}], "
                          f"absolute difference = {abs(intercept)} percentage points.")
        return self.accept_intercept_zero

    def check_extrapolation(self):
        """
        Check whether the computed requirement limit lies outside the supplied deviations.

        The method checks if the requirement has been computed,
        if not raises an error asking to compute the requirement first.
        The method warns if the computed requirement limit is outside the range of the provided deviations.

        Returns
        -------
        extrapolation_needed : bool
            ``True`` if the requirement limit is outside the provided ``deviations`` range.

        Raises
        ------
        RuntimeError
            If the requirement has not been computed yet.
        """
        # Check if the requirement has been computed, if not raise an error
        if self.requirement is None:
            raise RuntimeError("Requirement not computed: "
                               "please run `get_requirement()` before calling `check_extrapolation()`.")

        # Check if the computed requirement limit is outside the range of the provided deviations
        limit = self.requirement[0]
        self.extrapolation_needed = (limit < self.deviations.min() or limit > self.deviations.max())

        # Warn if extrapolation is needed to meet the target requirement
        if self.extrapolation_needed:
            warnings.warn(f"The computed requirement limit ({limit}%) is outside the range of the provided deviations "
                          f"({self.deviations.min()}% to {self.deviations.max()}%). "
                          f"Extrapolation is needed to meet the target requirement, "
                          f"which may lead to unreliable estimates.")
        return self.extrapolation_needed

    def plot_fit(self, ax=None, data_color=None, data_label=None, fit_color=None, fit_label=None, x_label=None,
                 y_label=None, title=None, show=True):
        """
        Plot the data points and the fitted linear model.

        The method checks if the model has been fitted, if not raises an error asking to fit the model first.
        The method generates points for the fitted line based on the fitted model parameters.
        The method creates a scatter plot of the data points and a line plot of the fitted model.
        The method allows customization of plot aesthetics through the parameters.

        Parameters
        ----------
        ax : matplotlib.axes.Axes, optional
            Axes to draw on. If ``None``, a new figure and axes are created.
        data_color, fit_color : str, optional
            Colors for data points and fitted line.
        data_label, fit_label : str, optional
            Legend labels for data and fit.
        x_label, y_label : str, optional
            Axis labels. Defaults provided if ``None``.
        title : str, optional
            Plot title. Defaults to a descriptive title if ``None``.
        show : bool, optional
            If ``True`` (default), call ``plt.show()`` before returning.

        Returns
        -------
        ax : matplotlib.axes.Axes
            The axes containing the plot.

        Raises
        ------
        RuntimeError
            If the model has not been fitted.
        """
        # Check if the model has been fitted, if not raise an error
        if self.x is None or self.y is None or self.sm_results is None:
            raise RuntimeError("Model not fitted: please run `fit_model()` before calling `plot_fit()`.")

        # Set default values for plot aesthetics if not provided
        default_title = f"{self.parameter} variation for {self.quality} {self.quantity} {self.angle}º"
        title = title if title is not None else default_title
        data_color = data_color if data_color is not None else "blue"
        data_label = data_label if data_label is not None else "Data"
        fit_color = fit_color if fit_color is not None else "green"
        fit_label = fit_label if fit_label is not None else "Linear fit"
        x_label = x_label if x_label is not None else f"Parameter {self.parameter} deviation (%)"
        y_label = y_label if y_label is not None else "Mean conversion coefficient deviation (%)"

        # Generate points for the fitted line
        xs = np.linspace(self.x.min(), self.x.max(), 200)
        intercept, slope = self.sm_results.params
        ys = intercept + slope * xs

        # Create the plot if no axes were provided
        if ax is None:
            fig, ax = plt.subplots()

        # Plot the data points and the fitted line
        ax.scatter(self.x, self.y, color=data_color, label=data_label)
        ax.plot(xs, ys, color=fit_color, label=fit_label)
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.set_title(title)
        ax.grid(True)
        ax.legend()

        # Show the plot if requested
        if show:
            plt.show()
        return ax

    def plot_residuals(self, ax=None, title=None, show=True):
        """
        Plot residuals versus fitted values to assess fit assumptions.

        The method checks if the model has been fitted, if not raises an error asking to fit the model first.
        The method retrieves the fitted values and residuals from the fitted model results.
        The method creates a scatter plot of residuals versus fitted values,
        with a horizontal line at zero to help visualize the distribution of residuals.
        The method allows customization of plot aesthetics through the parameters.

        Parameters
        ----------
        ax : matplotlib.axes.Axes, optional
            Axes to draw on. If ``None``, a new figure and axes are created.
        title : str, optional
            Plot title. Defaults to a descriptive title if ``None``.
        show : bool, optional
            If ``True`` (default), call ``plt.show()`` before returning.

        Returns
        -------
        ax : matplotlib.axes.Axes
            The axes containing the residuals plot.

        Raises
        ------
        RuntimeError
            If the model has not been fitted.
        """
        # Check if the model has been fitted, if not raise an error
        if self.sm_results is None:
            raise RuntimeError("Model not fitted: please run `fit_model()` before calling `plot_residuals()`.")

        # Set default title if not provided
        default_title = f"{self.parameter} variation for {self.quality} {self.quantity} {self.angle}º"
        title = title if title is not None else default_title

        # Get fitted values and residuals from the fitted model
        fitted = self.sm_results.fittedvalues
        resid = self.sm_results.resid

        # Create the plot if no axes were provided
        if ax is None:
            fig, ax = plt.subplots()

        # Plot residuals vs fitted values
        ax.scatter(fitted, resid)
        ax.axhline(0, color="k")
        ax.set_xlabel("Fitted")
        ax.set_ylabel("Residuals")
        ax.set_title(title)
        ax.grid(True)

        # Show the plot if requested
        if show:
            plt.show()
        return ax
