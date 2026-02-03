import importlib.resources as resources

import pandas as pd


class OperationalQuantities:
    """
    Catalog of operational dose quantities and supported irradiation angles.

    This small helper centralizes metadata used across the project for
    operational quantities such as directional, ambient and personal dose
    quantities (for example "H*(10)", "H'(0.07)", "Hp(3, cyl)"). The class
    exposes lookup and validation helpers so callers can enumerate known
    quantities, retrieve human-friendly symbols and verify supported
    irradiation angles.

    Attributes
    ----------
    operational_quantities : dict
        A shallow copy of the module-level `_OPERATIONAL_QUANTITIES` mapping
        where each key maps to a metadata dictionary with the following keys:
        ``symbol`` (str), ``type`` (str), ``depth`` (float|int), ``phantom``
        (str|None), and ``angles`` (list[int]).
    """
    # Operational quantities and irradiation angles
    _OPERATIONAL_QUANTITIES = {
        'h_prime_07': {
            'symbol': "H'(0.07)",
            'type': 'directional',
            'depth': 0.07,
            'phantom': None,
            'angles': [0, 15, 30, 45, 60, 75, 90, 180]
        },
        'h_prime_3': {
            'symbol': "H'(3)",
            'type': 'directional',
            'depth': 3,
            'phantom': None,
            'angles': [0, 15, 30, 45, 60, 75, 90, 180]
        },
        'h_star_10': {
            'symbol': "H*(10)",
            'type': 'ambient',
            'depth': 10,
            'phantom': None,
            'angles': [0]
        },
        'H_p_07_rod': {
            'symbol': "Hp(0.07, rod)",
            'type': 'personal',
            'depth': 0.07,
            'phantom': 'rod',
            'angles': [0]
        },
        'H_p_07_pill': {
            'symbol': "Hp(0.07, pillar)",
            'type': 'personal',
            'depth': 0.07,
            'phantom': 'pillar',
            'angles': [0]
        },
        'H_p_07_slab': {
            'symbol': "Hp(0.07, slab)",
            'type': 'personal',
            'depth': 0.07,
            'phantom': 'slab',
            'angles': [0, 15, 30, 45, 60, 75]
        },
        'H_p_3_cyl': {
            'symbol': "Hp(3, cyl)",
            'type': 'personal',
            'depth': 3,
            'phantom': 'cylinder',
            'angles': [0, 15, 30, 45, 60, 75, 90]
        },
        'H_p_10_slab': {
            'symbol': "Hp(10, slab)",
            'type': 'personal',
            'depth': 10,
            'phantom': 'slab',
            'angles': [0, 15, 30, 45, 60, 75]
        },
    }

    def __init__(self):
        """
        Initialize an OperationalQuantities instance.

        The constructor creates a shallow copy of the internal mapping and
        exposes it on the :pyattr:`operational_quantities` attribute so callers
        may inspect metadata without modifying the module-level constant.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.operational_quantities = dict(self._OPERATIONAL_QUANTITIES)

    def get_all_quantities(self, symbol=False):
        """
        Return the list of known quantities.

        Parameters
        ----------
        symbol : bool, optional
            If True, return the human-friendly symbols (the ``symbol`` field)
            for each quantity; otherwise return the internal keys. Default is
            False.

        Returns
        -------
        list of str
            A list of either internal keys or human symbols for all known
            operational quantities.
        """
        if symbol:
            return [quantity['symbol'] for quantity in self.operational_quantities.values()]
        else:
            return list(self.operational_quantities.keys())

    def is_quantity(self, quantity):
        """
        Check whether an internal quantity key is known.

        Parameters
        ----------
        quantity : str
            The internal key of the quantity to check (e.g. 'h_star_10').

        Returns
        -------
        bool
            True if the quantity exists, False otherwise.
        """
        return quantity in self.operational_quantities

    def is_quantity_angle(self, quantity, angle):
        """
        Check whether a given irradiation angle is supported for a quantity.

        Parameters
        ----------
        quantity : str
            Internal quantity key (e.g. 'h_prime_3').
        angle : int
            Irradiation angle in degrees to validate.

        Returns
        -------
        bool
            True if the quantity exists and the angle is supported; False
            otherwise.
        """
        if self.is_quantity(quantity) and angle in self.operational_quantities[quantity]['angles']:
            return True
        else:
            return False

    def get_quantity(self, quantity):
        """
        Retrieve the metadata dictionary for a known quantity.

        Parameters
        ----------
        quantity : str
            Internal quantity key to retrieve (e.g. 'h_p_07_slab').

        Returns
        -------
        dict
            Metadata dictionary for the requested quantity. The dict contains
            keys: ``symbol``, ``type``, ``depth``, ``phantom``, ``angles``.

        Raises
        ------
        ValueError
            If the requested quantity is unknown.
        """
        if self.is_quantity(quantity):
            return self.operational_quantities[quantity]
        else:
            raise ValueError(f'{quantity} is not an x-ray operational quantity.')

    def get_irradiation_angles(self, quantity):
        """
        Return the list of supported irradiation angles for a quantity.

        Parameters
        ----------
        quantity : str
            Internal quantity key (e.g. 'h_star_10').

        Returns
        -------
        list of int
            Ordered list of supported irradiation angles (degrees).

        Raises
        ------
        ValueError
            If the requested quantity is unknown.
        """
        q = self.get_quantity(quantity)
        return q['angles']

    def get_symbol(self, quantity):
        """
        Return the human-friendly symbol for a quantity.

        Parameters
        ----------
        quantity : str
            Internal quantity key (e.g. 'h_p_10_slab').

        Returns
        -------
        str
            Human-friendly printed symbol (for example "H*(10)").

        Raises
        ------
        ValueError
            If the requested quantity is unknown.
        """
        q = self.get_quantity(quantity)
        return q['symbol']


def get_mu_tr_over_rho_air(source='pene_2018', custom=(None, None)):
    """
    Return mono-energetic mass transfer coefficients of air.

    The function provides tabulated values of the mass transfer
    coefficient air (μ_tr/ρ, cm^2/g) as a function of photon energy (keV).
    By default the values are loaded from the bundled PENELOPE 2018
    CSV table; users may supply a custom (energies, values) pair.

    Parameters
    ----------
    source : {'pene_2018', 'custom'}, optional
        The source of the tabulated data. ``'pene_2018'`` (default) loads
        the bundled PENELOPE 2018 table shipped with the package. If
        ``'custom'`` is selected the ``custom`` parameter is returned
        directly.
    custom : tuple, optional
        When ``source='custom'`` this should be a two-tuple ``(energies, values)``
        where ``energies`` and ``values`` are sequence-like (for example
        lists, tuples or NumPy arrays) of identical length.
        Units must be keV for ``energies`` and cm^2/g for ``values``.
        Ignored when ``source='pene_2018'``.

    Returns
    -------
    tuple
        A two-tuple ``(energies, values)`` where both elements are 1-D
        NumPy arrays. ``energies`` gives photon energies in keV and
        ``values`` gives the corresponding ``mu_tr/rho`` values in
        cm^2 / g.

    Raises
    ------
    FileNotFoundError
        If the bundled PENELOPE CSV can not be located or read from the
        package resources.
    ValueError
        If ``source`` is not one of the supported options.

    Notes
    -----
    The bundled data file is read using :mod:`importlib.resources` so the
    function works when the package is installed as a wheel or when code
    is executed from a different working directory.

    The PENELOPE CSV is expected to contain columns named
    ``'Energy (keV)'`` and ``'μtr/ρ (cm2/g)'``; these column names are used
    to extract the returned arrays.
    """
    # Load PENELOPE 2018 data
    if source == 'pene_2018':

        # Load data from package resources
        try:
            pkg = 'metpyx.data.tables.mu_tr_over_rho_air'
            data_file = resources.files(pkg).joinpath('pene_2018.csv')
            with data_file.open('r', encoding='utf-8') as fh:
                df = pd.read_csv(fh)
        except Exception as exc:
            raise FileNotFoundError(f"Could not load 'pene_2018.csv' from package data:\n{exc}") from exc

        # Extract arrays
        energies = df['Energy (keV)'].values
        values = df['μtr/ρ (cm2/g)'].values
        return energies, values

    # Custom data provided by user
    elif source == 'custom':
        return custom

    # If we reach here, the source is invalid
    else:
        err_msg = f'Source of mass transfer coefficients of air must be "pene_2018" or "custom". Found: {source}'
        raise ValueError(err_msg)


def get_h_k(source='cmi_2025', quantity=None, angle=None, custom=(None, None)):
    """
    Return air kerma to dose conversion coefficients (h_K, Sv/Gy) for a given operational quantity and angle.

    The function loads tabulated h_K coefficients from the bundled CMI 2025
    tables. Each CSV file for a given quantity contains energy-dependent
    coefficients; the column selected depends on the irradiation angle.
    Users may also provide custom data via the ``custom`` parameter.

    Parameters
    ----------
    source : {'cmi_2025', 'custom'}, optional
        Data source to use. ``'cmi_2025'`` (default) loads the bundled CMI
        2025 coefficients. ``'custom'`` returns the supplied ``custom``
        tuple directly.
    quantity : str
        Internal operational quantity key (see :class:`OperationalQuantities`),
        for example ``'h_p_10_slab'``. Required when ``source='cmi_2025'``.
    angle : int
        Irradiation angle in degrees. Must be supported by the requested
        quantity (validated via :class:`OperationalQuantities`). Required
        when ``source='cmi_2025'``.
    custom : tuple, optional
        When ``source='custom'``, a two-tuple ``(energies, values)`` where
        both elements are sequence-like (lists, arrays) of equal length.
        Units must be keV for ``energies`` and Sv/Gy for ``values``.

    Returns
    -------
    tuple
        A two-tuple ``(energies, values)`` where both elements are 1-D
        NumPy arrays: ``energies`` in keV and ``values`` containing the
        corresponding ``hK`` coefficients in Sv/Gy.

    Raises
    ------
    ValueError
        If ``source`` is invalid, or if ``quantity``/``angle`` are not
        provided or invalid for the selected quantity.
    FileNotFoundError
        If the requested CSV file cannot be located or read from the
        package resources.

    Notes
    -----
    The function uses :mod:`importlib.resources` to read packaged CSVs so
    it works whether the package is a directory on disk or installed as a
    wheel. The expected CSV layout uses a column named ``'E keV'`` for the
    energies and a column named like ``'hK {angle} Sv/Gy'`` for the
    coefficient corresponding to ``angle`` degrees.
    """
    # Load CMI 2025 data
    if source == 'cmi_2025':

        # Validate quantity and angle
        if not OperationalQuantities().is_quantity_angle(quantity, angle):
            raise ValueError(f'Quantity {quantity} does not support angle {angle} degrees.')

        # Load data from package resources
        try:
            pkg = 'metpyx.data.tables.h_k_coeffs'
            data_file = resources.files(pkg).joinpath(f'cmi_2025/{quantity}.csv')
            with data_file.open('r', encoding='utf-8') as fh:
                df = pd.read_csv(fh)
        except Exception as exc:
            raise FileNotFoundError(f"Could not load 'cmi_2025/{quantity}.csv' from package data:\n{exc}") from exc

        # Extract arrays
        energies = df['E keV'].values
        values = df[f'hK {angle} Sv/Gy'].values
        return energies, values

    # Custom data provided by user
    elif source == 'custom':
        return custom

    # If we reach here, the source is invalid
    else:
        err_msg = f'Source of mass transfer coefficients of air must be "cmi_2025" or "custom". Found: {source}'
        raise ValueError(err_msg)
