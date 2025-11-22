import metpyx.data as dt


class XrayQualities:
    """
    A class to represent and manage X-ray radiation qualities.

    Attributes:
    -----------
    series : list
        A list of the X-ray radiation quality series.
    l_series : list
        A list of the L series radiation qualities.
    n_series : list
        A list of the N series radiation qualities.
    w_series : list
        A list of the W series radiation qualities.
    h_series : list
        A list of the H series radiation qualities.

    Methods:
    --------
    is_series(series):
        Checks if the given series is an x-ray radiation quality series.
    is_quality(quality):
        Checks if the given quality is an x-ray radiation quality.
    get_series_qualities(series):
        Retrieves the radiation qualities of the given radiation quality series.
    get_series(quality):
        Retrieves the series from the given radiation quality.
    get_peak_kilovoltage(quality):
        Retrieves the peak kilovoltage from the given radiation quality.
    get_filtration_thickness(quality):
        Retrieves the filtration thickness for the given radiation quality.
    """

    def __init__(self):
        """
        Initializes an XrayQualities object with radiation quality series.
        """
        self.series = list(dt.SERIES.keys())
        self.l_series = dt.SERIES['L']
        self.n_series = dt.SERIES['N']
        self.w_series = dt.SERIES['W']
        self.h_series = dt.SERIES['H']

    def is_series(self, series):
        """
        Checks if the given series is an x-ray radiation quality series.

        Args:
            series (str): The series to be checked.

        Returns:
            bool: True if the series is an x-ray radiation quality series, otherwise False.
        """
        if series in self.series:
            return True
        else:
            return False

    def is_quality(self, quality):
        """
        Checks if the given quality is an x-ray radiation quality.

        Args:
            quality (str): The radiation quality to be checked.

        Returns:
            bool: True if the quality is an x-ray radiation quality, otherwise False.
        """
        series = quality[0]
        if self.is_series(series):
            if quality in self.get_series_qualities(series):
                return True
            else:
                return False
        else:
            return False

    def get_series_qualities(self, series):
        """
        Retrieves the radiation qualities of the given radiation quality series.

        Args:
            series (str): The series whose qualities are to be retrieved.

        Returns:
            list: A list containing the qualities of the given radiation quality series.

        Raises:
            ValueError: If the given series is not an x-ray radiation quality series.
        """
        if self.is_series(series):
            return dt.SERIES[series]
        else:
            raise ValueError(f'{series} is not an x-ray radiation quality series.')

    def get_series(self, quality):
        """
        Retrieves the series from the given radiation quality.

        Args:
            quality (str): The radiation quality whose series is to be retrieved.

        Returns:
            str: The series corresponding to the given radiation quality.

        Raises:
            ValueError: If the quality is not an x-ray radiation quality.
        """
        if self.is_quality(quality):
            return quality[0]
        else:
            raise ValueError(f'{quality} is not an x-ray radiation quality.')

    def get_peak_kilovoltage(self, quality):
        """
        Retrieves the peak kilovoltage from the given radiation quality.

        Args:
            quality (str): The radiation quality whose peak kilovoltage is to be retrieved.

        Returns:
            int: The peak kilovoltage corresponding to the given radiation quality.

        Raises:
            ValueError: If the quality is not an x-ray radiation quality.
        """
        if self.is_quality(quality):
            return int(quality[1:])
        else:
            raise ValueError(f'{quality} is not an x-ray radiation quality.')

    def get_filtration_thickness(self, quality):
        """
        Retrieves the filtration thickness for the given radiation quality.

        Args:
            quality (str): The radiation quality whose filtration thickness is to be retrieved.

        Returns:
            dict: The filtration thickness corresponding to the given radiation quality.

        Raises:
            ValueError: If the quality is not an x-ray radiation quality.
        """
        if self.is_quality(quality):
            series = self.get_series(quality)
            return dt.TOTAL_FILTRATION[series][quality]
        else:
            raise ValueError(f'{quality} is not an x-ray radiation quality.')
