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
