class Qualities:
    """
    Manage X-ray radiation qualities and their filtration data.

    This class provides access to standard X‑ray quality series and
    per-quality inherent and additional filtration specifications. It
    exposes convenience methods to validate series/quality names and to
    retrieve series, peak kilovoltage and filtration components.

    Attributes
    ----------
    SERIES : dict
        Mapping of series letter to list of quality names.
    INHERENT_FILTRATION : dict
        Nested mapping of inherent filtration: {series: {quality: {material: thickness}}}.
    ADDITIONAL_FILTRATION : dict
        Nested mapping of additional filtration: {series: {quality: {material: thickness}}}.
    series : list
        List of available series letters.
    l_series, n_series, w_series, h_series : list
        Lists of qualities for series 'L', 'N', 'W' and 'H' respectively.
    """
    #: Radiation quality series
    SERIES = {
        'L': ['L10', 'L20', 'L30', 'L35', 'L55', 'L70', 'L100', 'L125', 'L170', 'L210', 'L240'],
        'N': ['N10', 'N15', 'N20', 'N25', 'N30', 'N40', 'N60', 'N80', 'N100', 'N120', 'N150', 'N200', 'N250', 'N300',
              'N350', 'N400'],
        'W': ['W30', 'W40', 'W60', 'W80', 'W110', 'W150', 'W200', 'W250', 'W300'],
        'H': ['H10', 'H20', 'H30', 'H40', 'H60', 'H80', 'H100', 'H150', 'H200', 'H250', 'H280', 'H300', 'H350', 'H400']
    }
    #: Inherent filtration thickness for radiation qualities
    INHERENT_FILTRATION = {
        'L': {
            'L10': {'Be': 1},
            'L20': {'Be': 1},
            'L30': {'Be': 1},
            'L35': {'Al': 4},
            'L55': {'Al': 4},
            'L70': {'Al': 4},
            'L100': {'Al': 4},
            'L125': {'Al': 4},
            'L170': {'Al': 4},
            'L210': {'Al': 4},
            'L240': {'Al': 4},
        },
        'N': {
            'N10': {'Be': 1},
            'N15': {'Be': 1},
            'N20': {'Be': 1},
            'N25': {'Be': 1},
            'N30': {'Be': 1},
            'N40': {'Al': 4},
            'N60': {'Al': 4},
            'N80': {'Al': 4},
            'N100': {'Al': 4},
            'N120': {'Al': 4},
            'N150': {'Al': 4},
            'N200': {'Al': 4},
            'N250': {'Al': 4},
            'N300': {'Al': 4},
            'N350': {'Al': 4},
            'N400': {'Al': 4},
        },
        'W': {
            'W30': {'Be': 1},
            'W40': {'Be': 1},
            'W60': {'Al': 4},
            'W80': {'Al': 4},
            'W110': {'Al': 4},
            'W150': {'Al': 4},
            'W200': {'Al': 4},
            'W250': {'Al': 4},
            'W300': {'Al': 4},
        },
        'H': {
            'H10': {'Be': 1},
            'H20': {'Be': 1},
            'H30': {'Be': 1},
            'H40': {'Be': 1},
            'H60': {'Be': 1},
            'H80': {'Al': 4},
            'H100': {'Al': 4},
            'H150': {'Al': 4},
            'H200': {'Al': 4},
            'H250': {'Al': 4},
            'H280': {'Al': 4},
            'H300': {'Al': 4},
            'H350': {'Al': 4},
            'H400': {'Al': 4}
        }
    }
    #: Additional filtration thickness for radiation qualities
    ADDITIONAL_FILTRATION = {
        'L': {
            'L10': {'Al': 0.3},
            'L20': {'Al': 2},
            'L30': {'Cu': 0.18, 'Al': 4},
            'L35': {'Cu': 0.25},
            'L55': {'Cu': 1.2},
            'L70': {'Cu': 2.5},
            'L100': {'Cu': 0.5, 'Sn': 2},
            'L125': {'Cu': 1, 'Sn': 4},
            'L170': {'Cu': 1, 'Sn': 3, 'Pb': 1.5},
            'L210': {'Cu': 0.5, 'Sn': 2, 'Pb': 3.5},
            'L240': {'Cu': 0.5, 'Sn': 2, 'Pb': 5.5},
        },
        'N': {
            'N10': {'Al': 0.1},
            'N15': {'Al': 0.5},
            'N20': {'Al': 1},
            'N25': {'Al': 2},
            'N30': {'Al': 4},
            'N40': {'Cu': 0.21},
            'N60': {'Cu': 0.6},
            'N80': {'Cu': 2},
            'N100': {'Cu': 5},
            'N120': {'Sn': 1, 'Cu': 5},
            'N150': {'Sn': 2.5},
            'N200': {'Sn': 3, 'Pb': 1, 'Cu': 2},
            'N250': {'Sn': 2, 'Pb': 3, },
            'N300': {'Sn': 3, 'Pb': 5, },
            'N350': {'Sn': 4.5, 'Pb': 7, },
            'N400': {'Sn': 6, 'Pb': 10, },
        },
        'W': {
            'W30': {'Al': 2},
            'W40': {'Al': 4},
            'W60': {'Cu': 0.3},
            'W80': {'Cu': 0.5},
            'W110': {'Cu': 2},
            'W150': {'Sn': 1},
            'W200': {'Sn': 2},
            'W250': {'Sn': 4},
            'W300': {'Sn': 6.5},
        },
        'H': {
            'H10': {},
            'H20': {'Al': 0.15},
            'H30': {'Al': 0.5},
            'H40': {'Al': 1.0},
            'H60': {'Al': 3.9},
            'H80': {'Al': 3.2},
            'H100': {'Cu': 0.15},
            'H150': {'Cu': 0.5},
            'H200': {'Cu': 1},
            'H250': {'Cu': 1.6},
            'H280': {'Cu': 3},
            'H300': {'Cu': 2.2},
            'H350': {'Cu': 3.4},
            'H400': {'Cu': 4.7},
        },
    }

    def __init__(self):
        """
        Initialize a Qualities instance.

        Notes
        -----
        Sets convenience attributes for series and per-series quality lists.
        """
        self.series = list(self.SERIES.keys())
        self.l_series = self.SERIES['L']
        self.n_series = self.SERIES['N']
        self.w_series = self.SERIES['W']
        self.h_series = self.SERIES['H']

    def is_series(self, series):
        """
        Check whether a string is a valid radiation quality series.

        Parameters
        ----------
        series : str
            Single-letter series name (e.g. 'L', 'N', 'W', 'H').

        Returns
        -------
        bool
            True if *series* is one of the known series letters, otherwise False.
        """
        if series in self.series:
            return True
        else:
            return False

    def is_quality(self, quality):
        """
        Check whether a string is a valid radiation quality.

        Parameters
        ----------
        quality : str
            Quality name, where the first character denotes the series
            (e.g. 'N60', 'L30').

        Returns
        -------
        bool
            True if *quality* exists in the registered qualities, otherwise False.
        """
        series = quality[0]
        if self.is_series(series):
            if quality in self.get_qualities(series):
                return True
            else:
                return False
        else:
            return False

    def get_qualities(self, series):
        """
        Retrieve the list of qualities for a given series.

        Parameters
        ----------
        series : str
            Series letter (e.g. 'L', 'N', 'W', 'H').

        Returns
        -------
        list
            List of quality names for the requested series.

        Raises
        ------
        ValueError
            If *series* is not a known radiation quality series.
        """
        if self.is_series(series):
            return self.SERIES[series]
        else:
            raise ValueError(f'{series} is not an x-ray radiation quality series.')

    def get_series(self, quality):
        """
        Get the series letter for a given quality.

        Parameters
        ----------
        quality : str
            Quality name (e.g. 'N60').

        Returns
        -------
        str
            Single-letter series corresponding to *quality*.

        Raises
        ------
        ValueError
            If *quality* is not a recognized radiation quality.
        """
        if self.is_quality(quality):
            return quality[0]
        else:
            raise ValueError(f'{quality} is not an x-ray radiation quality.')

    def get_voltage(self, quality):
        """
        Return the numeric peak kilovoltage for a given quality.

        Parameters
        ----------
        quality : str
            Quality name where the numeric portion represents kV (e.g. 'H100').

        Returns
        -------
        int
            Peak kilovoltage parsed from the quality name.

        Raises
        ------
        ValueError
            If *quality* is not a recognized radiation quality.
        """
        if self.is_quality(quality):
            return int(quality[1:])
        else:
            raise ValueError(f'{quality} is not an x-ray radiation quality.')

    def get_filtration(self, quality, inherent=False, additional=False):
        """
        Retrieve filtration component(s) for a given radiation quality.

        The filtration information is split into inherent and additional
        components. This method can return either component separately or
        the concatenation of both (inherent first).

        Parameters
        ----------
        quality : str
            Radiation quality name (e.g. 'N60').
        inherent : bool, optional
            If True, return only the inherent filtration (default False).
        additional : bool, optional
            If True, return only the additional filtration (default False).

        Returns
        -------
        list of tuple
            List of *(material, thickness)* pairs. Thickness is given in mm.
            When neither *inherent* nor *additional* is requested the returned
            list is the concatenation of inherent then additional entries.

        Raises
        ------
        ValueError
            If *quality* is not a recognized radiation quality.
        """
        if self.is_quality(quality):
            series = self.get_series(quality)
            _inherent = list(self.INHERENT_FILTRATION[series][quality].items())
            _additional = list(self.ADDITIONAL_FILTRATION[series][quality].items())

            if inherent:
                return _inherent
            elif additional:
                return _additional
            else:
                return _inherent + _additional
        else:
            raise ValueError(f'{quality} is not an x-ray radiation quality.')


class Quantities:
    """
    Represent X‑ray operational quantities and their irradiation angles.

    This class exposes a mapping of operational dose/fluence quantities to
    the standard irradiation angles used in measurements and provides
    simple query methods.

    Attributes
    ----------
    OPERATIONAL_QUANTITIES : dict
        Mapping of quantity name to list of irradiation angles (degrees).
    operational_quantities : dict
        Instance reference to OPERATIONAL_QUANTITIES.
    """
    #: Operational quantities and irradiation angles
    OPERATIONAL_QUANTITIES = {
        "H'(0.07)": [0, 15, 30, 45, 60, 75, 90, 180],
        "H'(3)": [0, 15, 30, 45, 60, 75, 90, 180],
        "H*(10)": [0],
        "Hp(0.07, rod)": [0],
        "Hp(0.07, pillar)": [0],
        "Hp(0.07, slab)": [0, 15, 30, 45, 60, 75],
        "Hp(3, cyl)": [0, 15, 30, 45, 60, 75, 90],
        "Hp(10, slab)": [0, 15, 30, 45, 60, 75]
    }

    def __init__(self):
        """
        Initialize a Quantities instance.

        Notes
        -----
        The instance attribute *operational_quantities* references the class
        mapping for convenience.
        """
        self.operational_quantities = self.OPERATIONAL_QUANTITIES

    def is_quantity(self, quantity):
        """
        Determine whether a string is a known operational quantity.

        Parameters
        ----------
        quantity : str
            Quantity name to check (e.g. "H'(0.07)").

        Returns
        -------
        bool
            True if *quantity* is present in the operational quantities mapping.
        """
        if quantity in self.operational_quantities:
            return True
        else:
            return False

    def get_operational_quantities(self):
        """
        Get the list of available operational quantity names.

        Returns
        -------
        list
            List of quantity names defined in the class.
        """
        return list(self.OPERATIONAL_QUANTITIES.keys())

    def get_irradiation_angles(self, quantity):
        """
        Retrieve irradiation angles for a given operational quantity.

        Parameters
        ----------
        quantity : str
            Operational quantity name.

        Returns
        -------
        list
            List of irradiation angles (in degrees) associated with *quantity*.

        Raises
        ------
        ValueError
            If *quantity* is not a registered operational quantity.
        """
        if self.is_quantity(quantity):
            return self.OPERATIONAL_QUANTITIES[quantity]
        else:
            raise ValueError(f'{quantity} is not an x-ray operational quantity.')
