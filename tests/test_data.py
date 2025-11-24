# TODO: Add docstrings to module, classes and methods
import numpy as np
import numpy.testing as npt
import pytest

from metpyx.data import Qualities, Quantities


class TestQualities:
    def test_constructor(self):
        x = Qualities()

        result_series = x.series
        result_l = x.l_series
        result_n = x.n_series
        result_w = x.w_series
        result_h = x.h_series

        expected_series = ['L', 'N', 'W', 'H']
        expected_l_series = ['L10', 'L20', 'L30', 'L35', 'L55', 'L70', 'L100', 'L125', 'L170', 'L210', 'L240']
        expected_n_series = ['N10', 'N15', 'N20', 'N25', 'N30', 'N40', 'N60', 'N80', 'N100', 'N120', 'N150', 'N200',
                             'N250', 'N300', 'N350', 'N400']
        expected_w_series = ['W30', 'W40', 'W60', 'W80', 'W110', 'W150', 'W200', 'W250', 'W300']
        expected_h_series = ['H10', 'H20', 'H30', 'H40', 'H60', 'H80', 'H100', 'H150', 'H200', 'H250', 'H280', 'H300',
                             'H350', 'H400']

        assert result_series == expected_series, f'X-rays series, expected {expected_series}, got {result_series}.'
        assert result_l == expected_l_series, f'L series qualities, expected {expected_l_series}, got {result_l}.'
        assert result_n == expected_n_series, f'N series qualities, expected {expected_n_series}, got {result_n}.'
        assert result_w == expected_w_series, f'W series qualities, expected {expected_w_series}, got {result_w}.'
        assert result_h == expected_h_series, f'H series qualities, expected {expected_h_series}, got {result_h}.'

    def test_is_series(self):
        series = ['L', 'N', 'W', 'H', 'X']
        expected = [True, True, True, True, False]

        x = Qualities()
        for s, e in zip(series, expected):
            assert x.is_series(s) is e, f'{s} series, expected {e}, got {x.is_series(s)}'

    def test_is_quality(self):
        invalid = ['X10', 'L1000']
        l_series = ['L10', 'L20', 'L30', 'L35', 'L55', 'L70', 'L100', 'L125', 'L170', 'L210', 'L240']
        n_series = ['N10', 'N15', 'N20', 'N25', 'N30', 'N40', 'N60', 'N80', 'N100', 'N120', 'N150', 'N200', 'N250',
                    'N300', 'N350', 'N400']
        w_series = ['W30', 'W40', 'W60', 'W80', 'W110', 'W150', 'W200', 'W250', 'W300']
        h_series = ['H10', 'H20', 'H30', 'H40', 'H60', 'H80', 'H100', 'H150', 'H200', 'H250', 'H280', 'H300', 'H350',
                    'H400']

        x = Qualities()
        for quality in invalid:
            assert x.is_quality(quality) is False, f'{quality} quality, expected False, got {x.is_quality(quality)}.'
        for quality in l_series:
            assert x.is_quality(quality) is True, f'{quality} quality, expected True, got {x.is_quality(quality)}.'
        for quality in n_series:
            assert x.is_quality(quality) is True, f'{quality} quality, expected True, got {x.is_quality(quality)}.'
        for quality in w_series:
            assert x.is_quality(quality) is True, f'{quality} quality, expected True, got {x.is_quality(quality)}.'
        for quality in h_series:
            assert x.is_quality(quality) is True, f'{quality} quality, expected True, got {x.is_quality(quality)}.'

    def test_get_series_qualities_valid_series(self):
        series = ['L', 'N', 'W', 'H']
        l_series = ['L10', 'L20', 'L30', 'L35', 'L55', 'L70', 'L100', 'L125', 'L170', 'L210', 'L240']
        n_series = ['N10', 'N15', 'N20', 'N25', 'N30', 'N40', 'N60', 'N80', 'N100', 'N120', 'N150', 'N200', 'N250',
                    'N300', 'N350', 'N400']
        w_series = ['W30', 'W40', 'W60', 'W80', 'W110', 'W150', 'W200', 'W250', 'W300']
        h_series = ['H10', 'H20', 'H30', 'H40', 'H60', 'H80', 'H100', 'H150', 'H200', 'H250', 'H280', 'H300', 'H350',
                    'H400']

        expected = [l_series, n_series, w_series, h_series]

        x = Qualities()
        for s, e in zip(series, expected):
            assert x.get_qualities(s) == e, f'{s} series, expected {e}, got {x.get_qualities(s)}.'

    def test_get_series_qualities_invalid_series(self):
        x = Qualities()
        with pytest.raises(ValueError) as exc_info:
            x.get_qualities('X')
        assert f'X is not an x-ray radiation quality series.' in str(exc_info.value)

    def test_get_series_valid_quality(self):
        l_series = ['L10', 'L20', 'L30', 'L35', 'L55', 'L70', 'L100', 'L125', 'L170', 'L210', 'L240']
        n_series = ['N10', 'N15', 'N20', 'N25', 'N30', 'N40', 'N60', 'N80', 'N100', 'N120', 'N150', 'N200', 'N250',
                    'N300', 'N350', 'N400']
        w_series = ['W30', 'W40', 'W60', 'W80', 'W110', 'W150', 'W200', 'W250', 'W300']
        h_series = ['H10', 'H20', 'H30', 'H40', 'H60', 'H80', 'H100', 'H150', 'H200', 'H250', 'H280', 'H300', 'H350',
                    'H400']

        expected_l_series = ['L'] * len(l_series)
        expected_n_series = ['N'] * len(n_series)
        expected_w_series = ['W'] * len(w_series)
        expected_h_series = ['H'] * len(h_series)

        qualities = l_series + n_series + w_series + h_series
        expected = expected_l_series + expected_n_series + expected_w_series + expected_h_series

        x = Qualities()
        for q, e in zip(qualities, expected):
            assert x.get_series(q) == e, f'{q} quality, expected {e} series, got {x.get_series(q)} series.'

    def test_get_series_invalid_quality(self):
        qualities = ['X10', 'L0', 'N0', 'W0', 'H0']

        x = Qualities()
        for q in qualities:
            with pytest.raises(ValueError) as exc_info:
                x.get_series(q)
            assert f'{q} is not an x-ray radiation quality.' in str(exc_info.value)

    def test_peak_kilovoltage_valid_quality(self):
        l_series = ['L10', 'L20', 'L30', 'L35', 'L55', 'L70', 'L100', 'L125', 'L170', 'L210', 'L240']
        n_series = ['N10', 'N15', 'N20', 'N25', 'N30', 'N40', 'N60', 'N80', 'N100', 'N120', 'N150', 'N200', 'N250',
                    'N300', 'N350', 'N400']
        w_series = ['W30', 'W40', 'W60', 'W80', 'W110', 'W150', 'W200', 'W250', 'W300']
        h_series = ['H10', 'H20', 'H30', 'H40', 'H60', 'H80', 'H100', 'H150', 'H200', 'H250', 'H280', 'H300', 'H350',
                    'H400']

        expected_l_series = [10, 20, 30, 35, 55, 70, 100, 125, 170, 210, 240]
        expected_n_series = [10, 15, 20, 25, 30, 40, 60, 80, 100, 120, 150, 200, 250, 300, 350, 400]
        expected_w_series = [30, 40, 60, 80, 110, 150, 200, 250, 300]
        expected_h_series = [10, 20, 30, 40, 60, 80, 100, 150, 200, 250, 280, 300, 350, 400]

        qualities = l_series + n_series + w_series + h_series
        expected = expected_l_series + expected_n_series + expected_w_series + expected_h_series

        x = Qualities()
        for q, e in zip(qualities, expected):
            assert x.get_voltage(q) == e, f'{q} quality, expected {e} kV, got {x.get_voltage(q)} kV.'

    def test_peak_kilovoltage_invalid_quality(self):
        qualities = ['X10', 'L0', 'N0', 'W0', 'H0']
        x = Qualities()
        for q in qualities:
            with pytest.raises(ValueError) as exc_info:
                x.get_voltage(q)
            assert f'{q} is not an x-ray radiation quality.' in str(exc_info.value)

    def test_get_filtration_thickness_invalid_quality(self):
        qualities = ['X10', 'L0', 'N0', 'W0', 'H0']
        x = Qualities()
        for q in qualities:
            with pytest.raises(ValueError) as exc_info:
                x.get_filtration(q)
            assert f'{q} is not an x-ray radiation quality.' in str(exc_info.value)

    def test_get_filtration_inherent(self):
        x = Qualities()

        l_qualities = ['L10', 'L20', 'L30', 'L35', 'L55', 'L70', 'L100', 'L125', 'L170', 'L210', 'L240']
        n_qualities = ['N10', 'N15', 'N20', 'N25', 'N30', 'N40', 'N60', 'N80', 'N100', 'N120', 'N150', 'N200', 'N250',
                       'N300', 'N350', 'N400']
        w_qualities = ['W30', 'W40', 'W60', 'W80', 'W110', 'W150', 'W200', 'W250', 'W300']
        h_qualities = ['H10', 'H20', 'H30', 'H40', 'H60', 'H80', 'H100', 'H150', 'H200', 'H250', 'H280', 'H300', 'H350',
                       'H400']

        l_filtration = [[('Be', 1)], [('Be', 1)], [('Be', 1)], [('Al', 4)], [('Al', 4)], [('Al', 4)], [('Al', 4)],
                        [('Al', 4)], [('Al', 4)], [('Al', 4)], [('Al', 4)]]
        n_filtration = [[('Be', 1)], [('Be', 1)], [('Be', 1)], [('Be', 1)], [('Be', 1)], [('Al', 4)], [('Al', 4)],
                        [('Al', 4)], [('Al', 4)], [('Al', 4)], [('Al', 4)], [('Al', 4)], [('Al', 4)], [('Al', 4)],
                        [('Al', 4)], [('Al', 4)]]
        w_filtration = [[('Be', 1)], [('Be', 1)], [('Al', 4)], [('Al', 4)], [('Al', 4)], [('Al', 4)], [('Al', 4)],
                        [('Al', 4)], [('Al', 4)]]
        h_filtration = [[('Be', 1)], [('Be', 1)], [('Be', 1)], [('Be', 1)], [('Be', 1)], [('Al', 4)], [('Al', 4)],
                        [('Al', 4)], [('Al', 4)], [('Al', 4)], [('Al', 4)], [('Al', 4)], [('Al', 4)], [('Al', 4)]]

        qualities = l_qualities + n_qualities + w_qualities + h_qualities
        expected_filtration = l_filtration + n_filtration + w_filtration + h_filtration
        result_filtration = [x.get_filtration(q, inherent=True) for q in qualities]

        for q, r, e in zip(qualities, result_filtration, expected_filtration):
            assert r == e, f'{q} quality, expected {e}, got {r}'

    def test_get_filtration_additional(self):
        x = Qualities()

        l_qualities = ['L10', 'L20', 'L30', 'L35', 'L55', 'L70', 'L100', 'L125', 'L170', 'L210', 'L240']
        n_qualities = ['N10', 'N15', 'N20', 'N25', 'N30', 'N40', 'N60', 'N80', 'N100', 'N120', 'N150', 'N200', 'N250',
                       'N300', 'N350', 'N400']
        w_qualities = ['W30', 'W40', 'W60', 'W80', 'W110', 'W150', 'W200', 'W250', 'W300']
        h_qualities = ['H10', 'H20', 'H30', 'H40', 'H60', 'H80', 'H100', 'H150', 'H200', 'H250', 'H280', 'H300', 'H350',
                       'H400']

        l_filtration = [[('Al', 0.3)], [('Al', 2)], [('Cu', 0.18), ('Al', 4)], [('Cu', 0.25)], [('Cu', 1.2)],
                        [('Cu', 2.5)], [('Cu', 0.5), ('Sn', 2)], [('Cu', 1), ('Sn', 4)],
                        [('Cu', 1), ('Sn', 3), ('Pb', 1.5)], [('Cu', 0.5), ('Sn', 2), ('Pb', 3.5)],
                        [('Cu', 0.5), ('Sn', 2), ('Pb', 5.5)]]
        n_filtration = [[('Al', 0.1)], [('Al', 0.5)], [('Al', 1)], [('Al', 2)], [('Al', 4)], [('Cu', 0.21)],
                        [('Cu', 0.6)], [('Cu', 2)], [('Cu', 5)], [('Sn', 1), ('Cu', 5)], [('Sn', 2.5)],
                        [('Sn', 3), ('Pb', 1), ('Cu', 2)], [('Sn', 2), ('Pb', 3)], [('Sn', 3), ('Pb', 5)],
                        [('Sn', 4.5), ('Pb', 7)], [('Sn', 6), ('Pb', 10)]]
        w_filtration = [[('Al', 2)], [('Al', 4)], [('Cu', 0.3)], [('Cu', 0.5)], [('Cu', 2)], [('Sn', 1)], [('Sn', 2)],
                        [('Sn', 4)], [('Sn', 6.5)]]
        h_filtration = [[], [('Al', 0.15)], [('Al', 0.5)], [('Al', 1.0)], [('Al', 3.9)], [('Al', 3.2)], [('Cu', 0.15)],
                        [('Cu', 0.5)], [('Cu', 1)], [('Cu', 1.6)], [('Cu', 3)], [('Cu', 2.2)], [('Cu', 3.4)],
                        [('Cu', 4.7)]]

        qualities = l_qualities + n_qualities + w_qualities + h_qualities
        expected_filtration = l_filtration + n_filtration + w_filtration + h_filtration
        result_filtration = [x.get_filtration(q, additional=True) for q in qualities]

        for q, r, e in zip(qualities, result_filtration, expected_filtration):
            assert r == e, f'{q} quality, expected {e}, got {r}'

    def test_get_filtration_total(self):
        x = Qualities()

        l_qualities = ['L10', 'L20', 'L30', 'L35', 'L55', 'L70', 'L100', 'L125', 'L170', 'L210', 'L240']
        n_qualities = ['N10', 'N15', 'N20', 'N25', 'N30', 'N40', 'N60', 'N80', 'N100', 'N120', 'N150', 'N200', 'N250',
                       'N300', 'N350', 'N400']
        w_qualities = ['W30', 'W40', 'W60', 'W80', 'W110', 'W150', 'W200', 'W250', 'W300']
        h_qualities = ['H10', 'H20', 'H30', 'H40', 'H60', 'H80', 'H100', 'H150', 'H200', 'H250', 'H280', 'H300', 'H350',
                       'H400']

        l_filtration = [[('Be', 1), ('Al', 0.3)], [('Be', 1), ('Al', 2)], [('Be', 1), ('Cu', 0.18), ('Al', 4)],
                        [('Al', 4), ('Cu', 0.25)], [('Al', 4), ('Cu', 1.2)], [('Al', 4), ('Cu', 2.5)],
                        [('Al', 4), ('Cu', 0.5), ('Sn', 2)], [('Al', 4), ('Cu', 1), ('Sn', 4)],
                        [('Al', 4), ('Cu', 1), ('Sn', 3), ('Pb', 1.5)],
                        [('Al', 4), ('Cu', 0.5), ('Sn', 2), ('Pb', 3.5)],
                        [('Al', 4), ('Cu', 0.5), ('Sn', 2), ('Pb', 5.5)]]
        n_filtration = [[('Be', 1), ('Al', 0.1)], [('Be', 1), ('Al', 0.5)], [('Be', 1), ('Al', 1)],
                        [('Be', 1), ('Al', 2)], [('Be', 1), ('Al', 4)], [('Al', 4), ('Cu', 0.21)],
                        [('Al', 4), ('Cu', 0.6)], [('Al', 4), ('Cu', 2)], [('Al', 4), ('Cu', 5)],
                        [('Al', 4), ('Sn', 1), ('Cu', 5)], [('Al', 4), ('Sn', 2.5)],
                        [('Al', 4), ('Sn', 3), ('Pb', 1), ('Cu', 2)], [('Al', 4), ('Sn', 2), ('Pb', 3)],
                        [('Al', 4), ('Sn', 3), ('Pb', 5)], [('Al', 4), ('Sn', 4.5), ('Pb', 7)],
                        [('Al', 4), ('Sn', 6), ('Pb', 10)]]
        w_filtration = [[('Be', 1), ('Al', 2)], [('Be', 1), ('Al', 4)], [('Al', 4), ('Cu', 0.3)],
                        [('Al', 4), ('Cu', 0.5)], [('Al', 4), ('Cu', 2)], [('Al', 4), ('Sn', 1)],
                        [('Al', 4), ('Sn', 2)], [('Al', 4), ('Sn', 4)], [('Al', 4), ('Sn', 6.5)]]
        h_filtration = [[('Be', 1)], [('Be', 1), ('Al', 0.15)], [('Be', 1), ('Al', 0.5)], [('Be', 1), ('Al', 1.0)],
                        [('Be', 1), ('Al', 3.9)], [('Al', 4), ('Al', 3.2)], [('Al', 4), ('Cu', 0.15)],
                        [('Al', 4), ('Cu', 0.5)], [('Al', 4), ('Cu', 1)], [('Al', 4), ('Cu', 1.6)],
                        [('Al', 4), ('Cu', 3)], [('Al', 4), ('Cu', 2.2)], [('Al', 4), ('Cu', 3.4)],
                        [('Al', 4), ('Cu', 4.7)]]

        qualities = l_qualities + n_qualities + w_qualities + h_qualities
        expected_filtration = l_filtration + n_filtration + w_filtration + h_filtration
        result_filtration = [x.get_filtration(q) for q in qualities]

        for q, r, e in zip(qualities, result_filtration, expected_filtration):
            assert r == e, f'{q} quality, expected {e}, got {r}'

    def test_to_df(self):
        """
        Test Qualities.to_df returns a complete filtration/qualities table.

        Verifies that :meth:`Qualities.to_df` constructs a pandas DataFrame with
        one row per registered radiation quality and the expected columns.

        The test checks:
        - The DataFrame length equals the total number of qualities (series L, N, W, H).
        - Column names match the expected set including inherent and additional
          filtration columns for common materials.
        - The 'Quality' column preserves the expected ordering of qualities.
        - The 'Tube potential (kV)' values are parsed correctly from quality names.
        - Inherent and additional filtration columns contain the expected
          thickness values (in millimetres) or NaN where a material is not
          present for a given quality.
        """
        x = Qualities()
        df = x.to_df()
        result_length = len(df)
        result_columns = df.columns.tolist()
        result_qualities = df['Quality'].tolist()
        result_voltages = df['Tube potential (kV)'].tolist()
        result_inherent_be = df['Inherent filtration (mm Be)'].tolist()
        result_inherent_al = df['Inherent filtration (mm Al)'].tolist()
        result_additional_pb = df['Additional filtration (mm Pb)'].tolist()
        result_additional_sn = df['Additional filtration (mm Sn)'].tolist()
        result_additional_cu = df['Additional filtration (mm Cu)'].tolist()
        result_additional_al = df['Additional filtration (mm Al)'].tolist()

        length = 50
        columns = ['Quality', 'Tube potential (kV)', 'Inherent filtration (mm Be)', 'Inherent filtration (mm Al)',
                   'Additional filtration (mm Pb)', 'Additional filtration (mm Sn)', 'Additional filtration (mm Cu)',
                   'Additional filtration (mm Al)']
        qualities = ['L10', 'L20', 'L30', 'L35', 'L55', 'L70', 'L100', 'L125', 'L170', 'L210', 'L240', 'N10', 'N15',
                     'N20', 'N25', 'N30', 'N40', 'N60', 'N80', 'N100', 'N120', 'N150', 'N200', 'N250', 'N300', 'N350',
                     'N400', 'W30', 'W40', 'W60', 'W80', 'W110', 'W150', 'W200', 'W250', 'W300', 'H10', 'H20', 'H30',
                     'H40', 'H60', 'H80', 'H100', 'H150', 'H200', 'H250', 'H280', 'H300', 'H350', 'H400']
        voltages = [10, 20, 30, 35, 55, 70, 100, 125, 170, 210, 240, 10, 15, 20, 25, 30, 40, 60, 80, 100, 120, 150, 200,
                    250, 300, 350, 400, 30, 40, 60, 80, 110, 150, 200, 250, 300, 10, 20, 30, 40, 60, 80, 100, 150, 200,
                    250, 280, 300, 350, 400]
        inherent_be = [1.0, 1.0, 1.0, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 1.0, 1.0, 1.0,
                       1.0, 1.0, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan,
                       1.0, 1.0, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 1.0, 1.0, 1.0, 1.0, 1.0,
                       np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]
        inherent_al = [np.nan, np.nan, np.nan, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, np.nan, np.nan, np.nan, np.nan,
                       np.nan, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, np.nan, np.nan, 4.0, 4.0, 4.0,
                       4.0, 4.0, 4.0, 4.0, np.nan, np.nan, np.nan, np.nan, np.nan, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0,
                       4.0, 4.0]
        additional_pb = [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 1.5, 3.5, 5.5, np.nan, np.nan,
                         np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 1.0, 3.0, 5.0, 7.0,
                         10.0, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan,
                         np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]
        additional_sn = [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 2.0, 4.0, 3.0, 2.0, 2.0, np.nan, np.nan,
                         np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 1.0, 2.5, 3.0, 2.0, 3.0, 4.5, 6.0,
                         np.nan, np.nan, np.nan, np.nan, np.nan, 1.0, 2.0, 4.0, 6.5, np.nan, np.nan, np.nan, np.nan,
                         np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]
        additional_cu = [np.nan, np.nan, 0.18, 0.25, 1.2, 2.5, 0.5, 1.0, 1.0, 0.5, 0.5, np.nan, np.nan, np.nan, np.nan,
                         np.nan, 0.21, 0.6, 2.0, 5.0, 5.0, np.nan, 2.0, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan,
                         0.3, 0.5, 2.0, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan,
                         0.15, 0.5, 1.0, 1.6, 3.0, 2.2, 3.4, 4.7]
        additional_al = [0.3, 2.0, 4.0, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 0.1, 0.5, 1.0,
                         2.0, 4.0, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan,
                         np.nan, 2.0, 4.0, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 0.15, 0.5,
                         1.0, 3.9, 3.2, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]

        npt.assert_array_equal(np.asarray(result_length), np.asarray(length))
        npt.assert_array_equal(np.asarray(result_columns), np.asarray(columns))
        npt.assert_array_equal(np.asarray(result_qualities), np.asarray(qualities))
        npt.assert_array_equal(np.asarray(result_voltages), np.asarray(voltages))
        npt.assert_array_equal(np.asarray(result_inherent_be), np.asarray(inherent_be))
        npt.assert_array_equal(np.asarray(result_inherent_al), np.asarray(inherent_al))
        npt.assert_array_equal(np.asarray(result_additional_pb), np.asarray(additional_pb))
        npt.assert_array_equal(np.asarray(result_additional_sn), np.asarray(additional_sn))
        npt.assert_array_equal(np.asarray(result_additional_cu), np.asarray(additional_cu))
        npt.assert_array_equal(np.asarray(result_additional_al), np.asarray(additional_al))


class TestQuantities:
    def test_constructor(self):
        x = Quantities()
        result = list(x.operational_quantities.keys())
        expected = ["H'(0.07)", "H'(3)", "H*(10)", "Hp(0.07, rod)", "Hp(0.07, pillar)", "Hp(0.07, slab)", "Hp(3, cyl)",
                    "Hp(10, slab)"]
        assert result == expected, f'Operational quantities, expected {expected}, got {result}.'

    def test_is_quantity(self):
        quantities = ["H'(0.07)", "H'(3)", "H*(10)", "Hp(0.07, rod)", "Hp(0.07, pillar)", "Hp(0.07, slab)",
                      "Hp(3, cyl)", "Hp(10, slab)", "Foo"]
        expected = [True] * (len(quantities) - 1) + [False]
        x = Quantities()
        for q, e in zip(quantities, expected):
            assert x.is_quantity(q) is e, f'{q} quantity, expected {e}, got {x.is_quantity(q)}.'

    def test_get_operational_quantities(self):
        x = Quantities()
        result = x.get_operational_quantities()
        expected = ["H'(0.07)", "H'(3)", "H*(10)", "Hp(0.07, rod)", "Hp(0.07, pillar)", "Hp(0.07, slab)", "Hp(3, cyl)",
                    "Hp(10, slab)"]
        assert result == expected, f'Operational quantities, expected {expected}, got {result}.'

    def test_get_irradiation_angles_valid_quantity(self):
        angles = {
            "H'(0.07)": [0, 15, 30, 45, 60, 75, 90, 180],
            "H'(3)": [0, 15, 30, 45, 60, 75, 90, 180],
            "H*(10)": [0],
            "Hp(0.07, rod)": [0],
            "Hp(0.07, pillar)": [0],
            "Hp(0.07, slab)": [0, 15, 30, 45, 60, 75],
            "Hp(3, cyl)": [0, 15, 30, 45, 60, 75, 90],
            "Hp(10, slab)": [0, 15, 30, 45, 60, 75]
        }
        quantities = list(angles.keys())
        expected = [angles[q] for q in quantities]
        x = Quantities()
        for q, e in zip(quantities, expected):
            assert x.get_irradiation_angles(q) == e, f'{q} quantity, expected {e}, got {x.get_irradiation_angles(q)}.'

    def test_get_irradiation_angles_invalid_quantity(self):
        x = Quantities()
        with pytest.raises(ValueError) as exc_info:
            x.get_irradiation_angles('H')
        assert f'H is not an x-ray operational quantity.' in str(exc_info.value)
