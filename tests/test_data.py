# TODO: Add docstrings to module, classes and methods
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
