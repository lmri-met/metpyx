import pytest

from data.quantities import OperationalQuantities


class TestNoInputMethods:
    def test_get_all_quantities(self):
        q = OperationalQuantities()
        quantities = ['h_prime_07', 'h_prime_3', 'h_star_10', 'H_p_07_rod', 'H_p_07_pill', 'H_p_07_slab', 'H_p_3_cyl',
                      'H_p_10_slab']
        assert q.get_all_quantities() == quantities

    def test_get_all_quantities_symbols(self):
        q = OperationalQuantities()
        quantities = ["H'(0.07)", "H'(3)", 'H*(10)', 'Hp(0.07, rod)', 'Hp(0.07, pillar)', 'Hp(0.07, slab)',
                      'Hp(3, cyl)', 'Hp(10, slab)']
        assert q.get_all_quantities(symbol=True) == quantities


class TestValidInputs:
    def test_is_quantity_valid_quantities(self):
        q = OperationalQuantities()
        assert q.is_quantity('h_prime_07') == True
        assert q.is_quantity('h_prime_3') == True
        assert q.is_quantity('h_star_10') == True
        assert q.is_quantity('H_p_07_rod') == True
        assert q.is_quantity('H_p_07_pill') == True
        assert q.is_quantity('H_p_07_slab') == True
        assert q.is_quantity('H_p_3_cyl') == True
        assert q.is_quantity('H_p_10_slab') == True

    def test_is_quantity_angle_valid_combinations(self):
        q = OperationalQuantities()
        assert q.is_quantity_angle('h_prime_07', 0) == True
        assert q.is_quantity_angle('h_prime_07', 15) == True
        assert q.is_quantity_angle('h_prime_07', 30) == True
        assert q.is_quantity_angle('h_prime_07', 45) == True
        assert q.is_quantity_angle('h_prime_07', 60) == True
        assert q.is_quantity_angle('h_prime_07', 75) == True
        assert q.is_quantity_angle('h_prime_07', 90) == True
        assert q.is_quantity_angle('h_prime_07', 180) == True
        assert q.is_quantity_angle('h_prime_3', 0) == True
        assert q.is_quantity_angle('h_prime_3', 15) == True
        assert q.is_quantity_angle('h_prime_3', 30) == True
        assert q.is_quantity_angle('h_prime_3', 45) == True
        assert q.is_quantity_angle('h_prime_3', 60) == True
        assert q.is_quantity_angle('h_prime_3', 75) == True
        assert q.is_quantity_angle('h_prime_3', 90) == True
        assert q.is_quantity_angle('h_prime_3', 180) == True
        assert q.is_quantity_angle('h_star_10', 0) == True
        assert q.is_quantity_angle('H_p_07_rod', 0) == True
        assert q.is_quantity_angle('H_p_07_pill', 0) == True
        assert q.is_quantity_angle('H_p_07_slab', 0) == True
        assert q.is_quantity_angle('H_p_07_slab', 15) == True
        assert q.is_quantity_angle('H_p_07_slab', 30) == True
        assert q.is_quantity_angle('H_p_07_slab', 45) == True
        assert q.is_quantity_angle('H_p_07_slab', 60) == True
        assert q.is_quantity_angle('H_p_07_slab', 75) == True
        assert q.is_quantity_angle('H_p_3_cyl', 0) == True
        assert q.is_quantity_angle('H_p_3_cyl', 15) == True
        assert q.is_quantity_angle('H_p_3_cyl', 30) == True
        assert q.is_quantity_angle('H_p_3_cyl', 45) == True
        assert q.is_quantity_angle('H_p_3_cyl', 60) == True
        assert q.is_quantity_angle('H_p_3_cyl', 75) == True
        assert q.is_quantity_angle('H_p_3_cyl', 90) == True
        assert q.is_quantity_angle('H_p_10_slab', 0) == True
        assert q.is_quantity_angle('H_p_10_slab', 15) == True
        assert q.is_quantity_angle('H_p_10_slab', 30) == True
        assert q.is_quantity_angle('H_p_10_slab', 45) == True
        assert q.is_quantity_angle('H_p_10_slab', 60) == True
        assert q.is_quantity_angle('H_p_10_slab', 75) == True

    def test_get_irradiation_angles_valid_quantities(self):
        q = OperationalQuantities()
        assert q.get_irradiation_angles('h_prime_07') == [0, 15, 30, 45, 60, 75, 90, 180]
        assert q.get_irradiation_angles('h_prime_3') == [0, 15, 30, 45, 60, 75, 90, 180]
        assert q.get_irradiation_angles('h_star_10') == [0]
        assert q.get_irradiation_angles('H_p_07_rod') == [0]
        assert q.get_irradiation_angles('H_p_07_pill') == [0]
        assert q.get_irradiation_angles('H_p_07_slab') == [0, 15, 30, 45, 60, 75]
        assert q.get_irradiation_angles('H_p_3_cyl') == [0, 15, 30, 45, 60, 75, 90]
        assert q.get_irradiation_angles('H_p_10_slab') == [0, 15, 30, 45, 60, 75]

    def test_get_symbol_valid_quantities(self):
        q = OperationalQuantities()
        assert q.get_symbol('h_prime_07') == "H'(0.07)"
        assert q.get_symbol('h_prime_3') == "H'(3)"
        assert q.get_symbol('h_star_10') == "H*(10)"
        assert q.get_symbol('H_p_07_rod') == "Hp(0.07, rod)"
        assert q.get_symbol('H_p_07_pill') == "Hp(0.07, pillar)"
        assert q.get_symbol('H_p_07_slab') == "Hp(0.07, slab)"
        assert q.get_symbol('H_p_3_cyl') == "Hp(3, cyl)"
        assert q.get_symbol('H_p_10_slab') == "Hp(10, slab)"


class TestInvalidInputs:
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
