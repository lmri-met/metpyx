class Qualities:
    """
    Helper and lookup for x-ray radiation qualities and their filtrations.

    This class provides constants and convenience methods for working with
    predefined x-ray radiation quality series (L, N, W, H), their inherent
    filtration and additional filtration materials and thicknesses.

    Attributes
    ----------
    SERIES : dict
        Mapping of series code (e.g. 'L') to list of quality names (e.g. 'L10').
    INHERENT_FILTRATION : dict
        Mapping of series -> quality -> inherent filtration materials/thickness.
    ADDITIONAL_FILTRATION : dict
        Mapping of series -> quality -> additional filtration materials/thickness.
    series : list
        Instance attribute set in :py:meth:`__init__` containing available series keys.

    Notes
    -----
    Filtration values are returned as dictionaries mapping material (str) to
    thickness (float or int). The class methods validate provided quality and
    series values and raise :class:`ValueError` for unknown inputs.
    """
    # Radiation quality series
    SERIES = {
        'L': ['L10', 'L20', 'L30', 'L35', 'L55', 'L70', 'L100', 'L125', 'L170', 'L210', 'L240'],
        'N': ['N10', 'N15', 'N20', 'N25', 'N30', 'N40', 'N60', 'N80', 'N100', 'N120', 'N150', 'N200', 'N250', 'N300',
              'N350', 'N400'],
        'W': ['W30', 'W40', 'W60', 'W80', 'W110', 'W150', 'W200', 'W250', 'W300'],
        'H': ['H10', 'H20', 'H30', 'H40', 'H60', 'H80', 'H100', 'H150', 'H200', 'H250', 'H280', 'H300', 'H350', 'H400']
    }
    # Inherent filtration thickness for radiation qualities
    INHERENT_FILTRATION = {
        'L': {
            'L10':  {'Be': 1},
            'L20':  {'Be': 1},
            'L30':  {'Be': 1},
            'L35':  {'Al': 4},
            'L55':  {'Al': 4},
            'L70':  {'Al': 4},
            'L100': {'Al': 4},
            'L125': {'Al': 4},
            'L170': {'Al': 4},
            'L210': {'Al': 4},
            'L240': {'Al': 4},
        },
        'N': {
            'N10':  {'Be': 1},
            'N15':  {'Be': 1},
            'N20':  {'Be': 1},
            'N25':  {'Be': 1},
            'N30':  {'Be': 1},
            'N40':  {'Al': 4},
            'N60':  {'Al': 4},
            'N80':  {'Al': 4},
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
            'W30':  {'Be': 1},
            'W40':  {'Be': 1},
            'W60':  {'Al': 4},
            'W80':  {'Al': 4},
            'W110': {'Al': 4},
            'W150': {'Al': 4},
            'W200': {'Al': 4},
            'W250': {'Al': 4},
            'W300': {'Al': 4},
        },
        'H': {
            'H10':  {'Be': 1},
            'H20':  {'Be': 1},
            'H30':  {'Be': 1},
            'H40':  {'Be': 1},
            'H60':  {'Be': 1},
            'H80':  {'Al': 4},
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
    # Additional filtration thickness for radiation qualities
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

        Sets the ``series`` attribute to the list of available series keys.
        """
        self.series = list(self.SERIES.keys())

    def is_series(self, series):
        """
        Check whether a given series code is available.

        Parameters
        ----------
        series : str
            Series code to check (e.g. 'L', 'N', 'W', 'H').

        Returns
        -------
        bool
            True if the series is available, False otherwise.
        """
        return series in self.series

    def is_quality(self, quality):
        """
        Check whether a given quality name is known.

        Parameters
        ----------
        quality : str
            Quality name to check (for example 'L10').

        Returns
        -------
        bool
            True if the quality exists in any series, False otherwise.
        """
        return quality in self.get_all_qualities()

    def get_all_qualities(self):
        """
        Return a flat list of all quality names across series.

        Returns
        -------
        list of str
            All defined quality names (e.g. ['L10', 'L20', ...]).
        """
        all_qualities = []
        for series in self.series:
            all_qualities.extend(self.SERIES[series])
        return all_qualities

    def get_qualities(self, series):
        """
        Return the quality names for a specific series.

        Parameters
        ----------
        series : str
            Series code (e.g. 'L', 'N', 'W', 'H').

        Returns
        -------
        list of str
            Quality names belonging to the requested series.

        Raises
        ------
        ValueError
            If the provided series is not recognized.
        """
        if self.is_series(series):
            return self.SERIES[series]
        else:
            raise ValueError(f'{series} is not an x-ray radiation quality series.')

    def get_series(self, quality):
        """
        Return the series code for a given quality name.

        Parameters
        ----------
        quality : str
            Quality name (e.g. 'N100').

        Returns
        -------
        str
            Single-character series code corresponding to the quality (e.g. 'N').

        Raises
        ------
        ValueError
            If the provided quality is not recognized.
        """
        if self.is_quality(quality):
            return quality[0]
        else:
            raise ValueError(f'{quality} is not an x-ray radiation quality.')

    def get_voltage(self, quality):
        """
        Return the numeric voltage portion of a quality name.

        Parameters
        ----------
        quality : str
            Quality name whose voltage portion should be returned (e.g. 'H200').

        Returns
        -------
        int
            Integer voltage parsed from the quality name (e.g. 200).

        Raises
        ------
        ValueError
            If the provided quality is not recognized.
        """
        if self.is_quality(quality):
            return int(quality[1:])
        else:
            raise ValueError(f'{quality} is not an x-ray radiation quality.')

    def get_filtration(self, quality, inherent=False, additional=False):
        """
        Return filtration material thicknesses for a quality.

        Parameters
        ----------
        quality : str
            Quality name (e.g. 'L30').
        inherent : bool, optional
            If True and ``additional`` is False return only inherent filtration.
            Default is False.
        additional : bool, optional
            If True and ``inherent`` is False return only additional filtration.
            Default is False.

        Returns
        -------
        dict
            Mapping of material (str) to thickness (float or int).
            If both ``inherent`` and ``additional`` are True or False,
            the returned dictionary contains the combined inherent and additional
            thicknesses (additional thickness summed on top of inherent).

        Raises
        ------
        ValueError
            If the provided quality is not recognized.
        """
        if self.is_quality(quality):
            series = self.get_series(quality)
            inherent_filtration = dict(self.INHERENT_FILTRATION[series][quality])
            additional_filtration = dict(self.ADDITIONAL_FILTRATION[series][quality])

            if inherent and not additional:
                return inherent_filtration
            elif additional and not inherent:
                return additional_filtration
            else:
                combined = dict(inherent_filtration)
                for material, thickness in additional_filtration.items():
                    combined[material] = combined.get(material, 0.0) + thickness
                return combined
        else:
            raise ValueError(f'{quality} is not an x-ray radiation quality.')
