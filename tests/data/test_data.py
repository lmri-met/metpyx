import pytest

from metpyx.data.coefficents import Coefficients
from metpyx.data.qualities import Qualities
from metpyx.data.quantities import OperationalQuantities


class TestQualitiesInvalidInputs:
    def test_is_series_invalid_series(self):
        q = Qualities()
        assert q.is_series('X') is False

    def test_is_quality_invalid_quality(self):
        q = Qualities()
        assert q.is_quality('X') is False

    def test_get_qualities_invalid_series(self):
        q = Qualities()
        with pytest.raises(ValueError) as exc_info:
            q.get_qualities('X')
        assert f'X is not an x-ray radiation quality series.' in str(exc_info.value)

    def test_get_series_invalid_qualities(self):
        q = Qualities()
        with pytest.raises(ValueError) as exc_info:
            q.get_series('X10')
        assert f'X10 is not an x-ray radiation quality.' in str(exc_info.value)

    def test_get_voltage_valid_qualities(self):
        q = Qualities()
        with pytest.raises(ValueError) as exc_info:
            q.get_voltage('X10')
        assert f'X10 is not an x-ray radiation quality.' in str(exc_info.value)

    def test_get_filtration_invalid_quality(self):
        q = Qualities()
        with pytest.raises(ValueError) as exc_info:
            q.get_filtration('X10')
        assert f'X10 is not an x-ray radiation quality.' in str(exc_info.value)


class TestQuantityInvalidInputs:
    def test_is_quantity_invalid_quantities(self):
        q = OperationalQuantities()
        assert q.is_quantity('X') == False

    def test_is_quantity_angle_invalid_quantity(self):
        q = OperationalQuantities()
        assert q.is_quantity_angle('x', 15) == False

    def test_is_quantity_angle_invalid_angle(self):
        q = OperationalQuantities()
        assert q.is_quantity_angle('h_star_10', 200) == False

    def test_is_quantity_angle_invalid_both(self):
        q = OperationalQuantities()
        assert q.is_quantity_angle('x', '15') == False

    def test_get_quantity_invalid_quantities(self):
        q = OperationalQuantities()
        with pytest.raises(ValueError) as exc_info:
            q.get_quantity('X')
        assert f'X is not an x-ray operational quantity.' in str(exc_info.value)


class TestCoefficientsInvalidInputs:
    def test_get_mu_tr_over_rho_air_invalid_source(self):
        q = Coefficients()
        with pytest.raises(ValueError) as exc_info:
            q.get_mu_tr_over_rho_air(source='invalid_source')
        assert f"Source must be one of ['pene_2018']. Found: invalid_source" in str(exc_info.value)

    def test_get_h_k_invalid_source(self):
        q = Coefficients()
        with pytest.raises(ValueError) as exc_info:
            q.get_h_k('h_star_10', 0, source='invalid_source')
        assert f"Source must be one of ['cmi_2025']. Found: invalid_source" in str(exc_info.value)

    def test_get_h_k_invalid_quantity(self):
        q = Coefficients()
        with pytest.raises(ValueError) as exc_info:
            q.get_h_k('x', 0)
        assert f'Quantity x at 0 degrees is not in predefined operational quantities.' in str(exc_info.value)

    def test_get_h_k_invalid_angle(self):
        q = Coefficients()
        with pytest.raises(ValueError) as exc_info:
            q.get_h_k('h_star_10', 300)
        assert f'Quantity h_star_10 at 300 degrees is not in predefined operational quantities.' in str(exc_info.value)
