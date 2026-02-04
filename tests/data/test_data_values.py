from metpyx.data.qualities import Qualities
from metpyx.data.quantities import OperationalQuantities


class TestQualitiesValues:
    def test_all_series(self):
        q = Qualities()
        assert q.get_all_series() == ['L', 'N', 'W', 'H']

    def test_all_qualities(self):
        q = Qualities()
        qualities = [
            'L10', 'L20', 'L30', 'L35', 'L55', 'L70', 'L100', 'L125', 'L170', 'L210', 'L240', 'N10', 'N15', 'N20',
            'N25', 'N30', 'N40', 'N60', 'N80', 'N100', 'N120', 'N150', 'N200', 'N250', 'N300', 'N350', 'N400', 'W30',
            'W40', 'W60', 'W80', 'W110', 'W150', 'W200', 'W250', 'W300', 'H10', 'H20', 'H30', 'H40', 'H60', 'H80',
            'H100', 'H150', 'H200', 'H250', 'H280', 'H300', 'H350', 'H400'
        ]
        assert q.get_all_qualities() == qualities

    def test_valid_series(self):
        q = Qualities()
        assert q.is_series('L') is True
        assert q.is_series('N') is True
        assert q.is_series('W') is True
        assert q.is_series('H') is True

    def test_valid_qualities(self):
        q = Qualities()
        assert q.is_quality('L10') == True
        assert q.is_quality('L20') == True
        assert q.is_quality('L30') == True
        assert q.is_quality('L35') == True
        assert q.is_quality('L55') == True
        assert q.is_quality('L70') == True
        assert q.is_quality('L100') == True
        assert q.is_quality('L125') == True
        assert q.is_quality('L170') == True
        assert q.is_quality('L210') == True
        assert q.is_quality('L240') == True
        assert q.is_quality('N10') == True
        assert q.is_quality('N15') == True
        assert q.is_quality('N20') == True
        assert q.is_quality('N25') == True
        assert q.is_quality('N30') == True
        assert q.is_quality('N40') == True
        assert q.is_quality('N60') == True
        assert q.is_quality('N80') == True
        assert q.is_quality('N100') == True
        assert q.is_quality('N120') == True
        assert q.is_quality('N150') == True
        assert q.is_quality('N200') == True
        assert q.is_quality('N250') == True
        assert q.is_quality('N300') == True
        assert q.is_quality('N350') == True
        assert q.is_quality('N400') == True
        assert q.is_quality('W30') == True
        assert q.is_quality('W40') == True
        assert q.is_quality('W60') == True
        assert q.is_quality('W80') == True
        assert q.is_quality('W110') == True
        assert q.is_quality('W150') == True
        assert q.is_quality('W200') == True
        assert q.is_quality('W250') == True
        assert q.is_quality('W300') == True
        assert q.is_quality('H10') == True
        assert q.is_quality('H20') == True
        assert q.is_quality('H30') == True
        assert q.is_quality('H40') == True
        assert q.is_quality('H60') == True
        assert q.is_quality('H80') == True
        assert q.is_quality('H100') == True
        assert q.is_quality('H150') == True
        assert q.is_quality('H200') == True
        assert q.is_quality('H250') == True
        assert q.is_quality('H280') == True
        assert q.is_quality('H300') == True
        assert q.is_quality('H350') == True
        assert q.is_quality('H400') == True

    def test_qualities_from_series(self):
        q = Qualities()
        l = ['L10', 'L20', 'L30', 'L35', 'L55', 'L70', 'L100', 'L125', 'L170', 'L210', 'L240']
        n = ['N10', 'N15', 'N20', 'N25', 'N30', 'N40', 'N60', 'N80', 'N100', 'N120', 'N150', 'N200', 'N250', 'N300',
             'N350', 'N400']
        w = ['W30', 'W40', 'W60', 'W80', 'W110', 'W150', 'W200', 'W250', 'W300']
        h = ['H10', 'H20', 'H30', 'H40', 'H60', 'H80', 'H100', 'H150', 'H200', 'H250', 'H280', 'H300', 'H350', 'H400']
        assert q.get_qualities('L') == l
        assert q.get_qualities('N') == n
        assert q.get_qualities('W') == w
        assert q.get_qualities('H') == h

    def test_series_from_qualities(self):
        q = Qualities()
        assert q.get_series('L10') == 'L'
        assert q.get_series('L20') == 'L'
        assert q.get_series('L30') == 'L'
        assert q.get_series('L35') == 'L'
        assert q.get_series('L55') == 'L'
        assert q.get_series('L70') == 'L'
        assert q.get_series('L100') == 'L'
        assert q.get_series('L125') == 'L'
        assert q.get_series('L170') == 'L'
        assert q.get_series('L210') == 'L'
        assert q.get_series('L240') == 'L'
        assert q.get_series('N10') == 'N'
        assert q.get_series('N15') == 'N'
        assert q.get_series('N20') == 'N'
        assert q.get_series('N25') == 'N'
        assert q.get_series('N30') == 'N'
        assert q.get_series('N40') == 'N'
        assert q.get_series('N60') == 'N'
        assert q.get_series('N80') == 'N'
        assert q.get_series('N100') == 'N'
        assert q.get_series('N120') == 'N'
        assert q.get_series('N150') == 'N'
        assert q.get_series('N200') == 'N'
        assert q.get_series('N250') == 'N'
        assert q.get_series('N300') == 'N'
        assert q.get_series('N350') == 'N'
        assert q.get_series('N400') == 'N'
        assert q.get_series('W30') == 'W'
        assert q.get_series('W40') == 'W'
        assert q.get_series('W60') == 'W'
        assert q.get_series('W80') == 'W'
        assert q.get_series('W110') == 'W'
        assert q.get_series('W150') == 'W'
        assert q.get_series('W200') == 'W'
        assert q.get_series('W250') == 'W'
        assert q.get_series('W300') == 'W'
        assert q.get_series('H10') == 'H'
        assert q.get_series('H20') == 'H'
        assert q.get_series('H30') == 'H'
        assert q.get_series('H40') == 'H'
        assert q.get_series('H60') == 'H'
        assert q.get_series('H80') == 'H'
        assert q.get_series('H100') == 'H'
        assert q.get_series('H150') == 'H'
        assert q.get_series('H200') == 'H'
        assert q.get_series('H250') == 'H'
        assert q.get_series('H280') == 'H'
        assert q.get_series('H300') == 'H'
        assert q.get_series('H350') == 'H'
        assert q.get_series('H400') == 'H'

    def test_voltage_from_quality(self):
        q = Qualities()
        assert q.get_voltage('L10') == 10
        assert q.get_voltage('L20') == 20
        assert q.get_voltage('L30') == 30
        assert q.get_voltage('L35') == 35
        assert q.get_voltage('L55') == 55
        assert q.get_voltage('L70') == 70
        assert q.get_voltage('L100') == 100
        assert q.get_voltage('L125') == 125
        assert q.get_voltage('L170') == 170
        assert q.get_voltage('L210') == 210
        assert q.get_voltage('L240') == 240
        assert q.get_voltage('N10') == 10
        assert q.get_voltage('N15') == 15
        assert q.get_voltage('N20') == 20
        assert q.get_voltage('N25') == 25
        assert q.get_voltage('N30') == 30
        assert q.get_voltage('N40') == 40
        assert q.get_voltage('N60') == 60
        assert q.get_voltage('N80') == 80
        assert q.get_voltage('N100') == 100
        assert q.get_voltage('N120') == 120
        assert q.get_voltage('N150') == 150
        assert q.get_voltage('N200') == 200
        assert q.get_voltage('N250') == 250
        assert q.get_voltage('N300') == 300
        assert q.get_voltage('N350') == 350
        assert q.get_voltage('N400') == 400
        assert q.get_voltage('W30') == 30
        assert q.get_voltage('W40') == 40
        assert q.get_voltage('W60') == 60
        assert q.get_voltage('W80') == 80
        assert q.get_voltage('W110') == 110
        assert q.get_voltage('W150') == 150
        assert q.get_voltage('W200') == 200
        assert q.get_voltage('W250') == 250
        assert q.get_voltage('W300') == 300
        assert q.get_voltage('H10') == 10
        assert q.get_voltage('H20') == 20
        assert q.get_voltage('H30') == 30
        assert q.get_voltage('H40') == 40
        assert q.get_voltage('H60') == 60
        assert q.get_voltage('H80') == 80
        assert q.get_voltage('H100') == 100
        assert q.get_voltage('H150') == 150
        assert q.get_voltage('H200') == 200
        assert q.get_voltage('H250') == 250
        assert q.get_voltage('H280') == 280
        assert q.get_voltage('H300') == 300
        assert q.get_voltage('H350') == 350
        assert q.get_voltage('H400') == 400

    def test_inherent_filtration_from_quality(self):
        q = Qualities()
        assert q.get_filtration('L10', inherent=True) == {'Be': 1}
        assert q.get_filtration('L20', inherent=True) == {'Be': 1}
        assert q.get_filtration('L30', inherent=True) == {'Be': 1}
        assert q.get_filtration('L35', inherent=True) == {'Al': 4}
        assert q.get_filtration('L55', inherent=True) == {'Al': 4}
        assert q.get_filtration('L70', inherent=True) == {'Al': 4}
        assert q.get_filtration('L100', inherent=True) == {'Al': 4}
        assert q.get_filtration('L125', inherent=True) == {'Al': 4}
        assert q.get_filtration('L170', inherent=True) == {'Al': 4}
        assert q.get_filtration('L210', inherent=True) == {'Al': 4}
        assert q.get_filtration('L240', inherent=True) == {'Al': 4}
        assert q.get_filtration('N10', inherent=True) == {'Be': 1}
        assert q.get_filtration('N15', inherent=True) == {'Be': 1}
        assert q.get_filtration('N20', inherent=True) == {'Be': 1}
        assert q.get_filtration('N25', inherent=True) == {'Be': 1}
        assert q.get_filtration('N30', inherent=True) == {'Be': 1}
        assert q.get_filtration('N40', inherent=True) == {'Al': 4}
        assert q.get_filtration('N60', inherent=True) == {'Al': 4}
        assert q.get_filtration('N80', inherent=True) == {'Al': 4}
        assert q.get_filtration('N100', inherent=True) == {'Al': 4}
        assert q.get_filtration('N120', inherent=True) == {'Al': 4}
        assert q.get_filtration('N150', inherent=True) == {'Al': 4}
        assert q.get_filtration('N200', inherent=True) == {'Al': 4}
        assert q.get_filtration('N250', inherent=True) == {'Al': 4}
        assert q.get_filtration('N300', inherent=True) == {'Al': 4}
        assert q.get_filtration('N350', inherent=True) == {'Al': 4}
        assert q.get_filtration('N400', inherent=True) == {'Al': 4}
        assert q.get_filtration('W30', inherent=True) == {'Be': 1}
        assert q.get_filtration('W40', inherent=True) == {'Be': 1}
        assert q.get_filtration('W60', inherent=True) == {'Al': 4}
        assert q.get_filtration('W80', inherent=True) == {'Al': 4}
        assert q.get_filtration('W110', inherent=True) == {'Al': 4}
        assert q.get_filtration('W150', inherent=True) == {'Al': 4}
        assert q.get_filtration('W200', inherent=True) == {'Al': 4}
        assert q.get_filtration('W250', inherent=True) == {'Al': 4}
        assert q.get_filtration('W300', inherent=True) == {'Al': 4}
        assert q.get_filtration('H10', inherent=True) == {'Be': 1}
        assert q.get_filtration('H20', inherent=True) == {'Be': 1}
        assert q.get_filtration('H30', inherent=True) == {'Be': 1}
        assert q.get_filtration('H40', inherent=True) == {'Be': 1}
        assert q.get_filtration('H60', inherent=True) == {'Be': 1}
        assert q.get_filtration('H80', inherent=True) == {'Al': 4}
        assert q.get_filtration('H100', inherent=True) == {'Al': 4}
        assert q.get_filtration('H150', inherent=True) == {'Al': 4}
        assert q.get_filtration('H200', inherent=True) == {'Al': 4}
        assert q.get_filtration('H250', inherent=True) == {'Al': 4}
        assert q.get_filtration('H280', inherent=True) == {'Al': 4}
        assert q.get_filtration('H300', inherent=True) == {'Al': 4}
        assert q.get_filtration('H350', inherent=True) == {'Al': 4}
        assert q.get_filtration('H400', inherent=True) == {'Al': 4}

    def test_additional_filtration_from_quality(self):
        q = Qualities()
        assert q.get_filtration('L10', additional=True) == {'Al': 0.3}
        assert q.get_filtration('L20', additional=True) == {'Al': 2}
        assert q.get_filtration('L30', additional=True) == {'Cu': 0.18, 'Al': 4}
        assert q.get_filtration('L35', additional=True) == {'Cu': 0.25}
        assert q.get_filtration('L55', additional=True) == {'Cu': 1.2}
        assert q.get_filtration('L70', additional=True) == {'Cu': 2.5}
        assert q.get_filtration('L100', additional=True) == {'Cu': 0.5, 'Sn': 2}
        assert q.get_filtration('L125', additional=True) == {'Cu': 1, 'Sn': 4}
        assert q.get_filtration('L170', additional=True) == {'Cu': 1, 'Sn': 3, 'Pb': 1.5}
        assert q.get_filtration('L210', additional=True) == {'Cu': 0.5, 'Sn': 2, 'Pb': 3.5}
        assert q.get_filtration('L240', additional=True) == {'Cu': 0.5, 'Sn': 2, 'Pb': 5.5}
        assert q.get_filtration('N10', additional=True) == {'Al': 0.1}
        assert q.get_filtration('N15', additional=True) == {'Al': 0.5}
        assert q.get_filtration('N20', additional=True) == {'Al': 1}
        assert q.get_filtration('N25', additional=True) == {'Al': 2}
        assert q.get_filtration('N30', additional=True) == {'Al': 4}
        assert q.get_filtration('N40', additional=True) == {'Cu': 0.21}
        assert q.get_filtration('N60', additional=True) == {'Cu': 0.6}
        assert q.get_filtration('N80', additional=True) == {'Cu': 2}
        assert q.get_filtration('N100', additional=True) == {'Cu': 5}
        assert q.get_filtration('N120', additional=True) == {'Sn': 1, 'Cu': 5}
        assert q.get_filtration('N150', additional=True) == {'Sn': 2.5}
        assert q.get_filtration('N200', additional=True) == {'Sn': 3, 'Pb': 1, 'Cu': 2}
        assert q.get_filtration('N250', additional=True) == {'Sn': 2, 'Pb': 3, }
        assert q.get_filtration('N300', additional=True) == {'Sn': 3, 'Pb': 5, }
        assert q.get_filtration('N350', additional=True) == {'Sn': 4.5, 'Pb': 7, }
        assert q.get_filtration('N400', additional=True) == {'Sn': 6, 'Pb': 10, }
        assert q.get_filtration('W30', additional=True) == {'Al': 2}
        assert q.get_filtration('W40', additional=True) == {'Al': 4}
        assert q.get_filtration('W60', additional=True) == {'Cu': 0.3}
        assert q.get_filtration('W80', additional=True) == {'Cu': 0.5}
        assert q.get_filtration('W110', additional=True) == {'Cu': 2}
        assert q.get_filtration('W150', additional=True) == {'Sn': 1}
        assert q.get_filtration('W200', additional=True) == {'Sn': 2}
        assert q.get_filtration('W250', additional=True) == {'Sn': 4}
        assert q.get_filtration('W300', additional=True) == {'Sn': 6.5}
        assert q.get_filtration('H10', additional=True) == {}
        assert q.get_filtration('H20', additional=True) == {'Al': 0.15}
        assert q.get_filtration('H30', additional=True) == {'Al': 0.5}
        assert q.get_filtration('H40', additional=True) == {'Al': 1.0}
        assert q.get_filtration('H60', additional=True) == {'Al': 3.9}
        assert q.get_filtration('H80', additional=True) == {'Al': 3.2}
        assert q.get_filtration('H100', additional=True) == {'Cu': 0.15}
        assert q.get_filtration('H150', additional=True) == {'Cu': 0.5}
        assert q.get_filtration('H200', additional=True) == {'Cu': 1}
        assert q.get_filtration('H250', additional=True) == {'Cu': 1.6}
        assert q.get_filtration('H280', additional=True) == {'Cu': 3}
        assert q.get_filtration('H300', additional=True) == {'Cu': 2.2}
        assert q.get_filtration('H350', additional=True) == {'Cu': 3.4}
        assert q.get_filtration('H400', additional=True) == {'Cu': 4.7}

    def test_total_filtration_from_quality(self):
        q = Qualities()
        assert q.get_filtration('L10') == {'Be': 1, 'Al': 0.3}
        assert q.get_filtration('L20') == {'Be': 1, 'Al': 2}
        assert q.get_filtration('L30') == {'Be': 1, 'Cu': 0.18, 'Al': 4}
        assert q.get_filtration('L35') == {'Al': 4, 'Cu': 0.25}
        assert q.get_filtration('L55') == {'Al': 4, 'Cu': 1.2}
        assert q.get_filtration('L70') == {'Al': 4, 'Cu': 2.5}
        assert q.get_filtration('L100') == {'Al': 4, 'Cu': 0.5, 'Sn': 2}
        assert q.get_filtration('L125') == {'Al': 4, 'Cu': 1, 'Sn': 4}
        assert q.get_filtration('L170') == {'Al': 4, 'Cu': 1, 'Sn': 3, 'Pb': 1.5}
        assert q.get_filtration('L210') == {'Al': 4, 'Cu': 0.5, 'Sn': 2, 'Pb': 3.5}
        assert q.get_filtration('L240') == {'Al': 4, 'Cu': 0.5, 'Sn': 2, 'Pb': 5.5}
        assert q.get_filtration('N10') == {'Be': 1, 'Al': 0.1}
        assert q.get_filtration('N15') == {'Be': 1, 'Al': 0.5}
        assert q.get_filtration('N20') == {'Be': 1, 'Al': 1}
        assert q.get_filtration('N25') == {'Be': 1, 'Al': 2}
        assert q.get_filtration('N30') == {'Be': 1, 'Al': 4}
        assert q.get_filtration('N40') == {'Al': 4, 'Cu': 0.21}
        assert q.get_filtration('N60') == {'Al': 4, 'Cu': 0.6}
        assert q.get_filtration('N80') == {'Al': 4, 'Cu': 2}
        assert q.get_filtration('N100') == {'Al': 4, 'Cu': 5}
        assert q.get_filtration('N120') == {'Al': 4, 'Sn': 1, 'Cu': 5}
        assert q.get_filtration('N150') == {'Al': 4, 'Sn': 2.5}
        assert q.get_filtration('N200') == {'Al': 4, 'Sn': 3, 'Pb': 1, 'Cu': 2}
        assert q.get_filtration('N250') == {'Al': 4, 'Sn': 2, 'Pb': 3, }
        assert q.get_filtration('N300') == {'Al': 4, 'Sn': 3, 'Pb': 5, }
        assert q.get_filtration('N350') == {'Al': 4, 'Sn': 4.5, 'Pb': 7, }
        assert q.get_filtration('N400') == {'Al': 4, 'Sn': 6, 'Pb': 10, }
        assert q.get_filtration('W30') == {'Be': 1, 'Al': 2}
        assert q.get_filtration('W40') == {'Be': 1, 'Al': 4}
        assert q.get_filtration('W60') == {'Al': 4, 'Cu': 0.3}
        assert q.get_filtration('W80') == {'Al': 4, 'Cu': 0.5}
        assert q.get_filtration('W110') == {'Al': 4, 'Cu': 2}
        assert q.get_filtration('W150') == {'Al': 4, 'Sn': 1}
        assert q.get_filtration('W200') == {'Al': 4, 'Sn': 2}
        assert q.get_filtration('W250') == {'Al': 4, 'Sn': 4}
        assert q.get_filtration('W300') == {'Al': 4, 'Sn': 6.5}
        assert q.get_filtration('H10') == {'Be': 1}
        assert q.get_filtration('H20') == {'Be': 1, 'Al': 0.15}
        assert q.get_filtration('H30') == {'Be': 1, 'Al': 0.5}
        assert q.get_filtration('H40') == {'Be': 1, 'Al': 1.0}
        assert q.get_filtration('H60') == {'Be': 1, 'Al': 3.9}
        assert q.get_filtration('H80') == {'Al': 7.2}
        assert q.get_filtration('H100') == {'Al': 4, 'Cu': 0.15}
        assert q.get_filtration('H150') == {'Al': 4, 'Cu': 0.5}
        assert q.get_filtration('H200') == {'Al': 4, 'Cu': 1}
        assert q.get_filtration('H250') == {'Al': 4, 'Cu': 1.6}
        assert q.get_filtration('H280') == {'Al': 4, 'Cu': 3}
        assert q.get_filtration('H300') == {'Al': 4, 'Cu': 2.2}
        assert q.get_filtration('H350') == {'Al': 4, 'Cu': 3.4}
        assert q.get_filtration('H400') == {'Al': 4, 'Cu': 4.7}


class TestQuantitiesValues:
    def test_all_quantities(self):
        q = OperationalQuantities()
        quantities = ['h_prime_07', 'h_prime_3', 'h_star_10', 'H_p_07_rod', 'H_p_07_pill', 'H_p_07_slab', 'H_p_3_cyl',
                      'H_p_10_slab']
        assert q.get_all_quantities() == quantities

    def test_all_symbols(self):
        q = OperationalQuantities()
        quantities = ["H'(0.07)", "H'(3)", 'H*(10)', 'Hp(0.07, rod)', 'Hp(0.07, pillar)', 'Hp(0.07, slab)',
                      'Hp(3, cyl)', 'Hp(10, slab)']
        assert q.get_all_quantities(symbol=True) == quantities

    def test_valid_quantities(self):
        q = OperationalQuantities()
        assert q.is_quantity('h_prime_07') == True
        assert q.is_quantity('h_prime_3') == True
        assert q.is_quantity('h_star_10') == True
        assert q.is_quantity('H_p_07_rod') == True
        assert q.is_quantity('H_p_07_pill') == True
        assert q.is_quantity('H_p_07_slab') == True
        assert q.is_quantity('H_p_3_cyl') == True
        assert q.is_quantity('H_p_10_slab') == True

    def test_valid_quantity_angle_combinations(self):
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

    def test_irradiation_angles_from_quantities(self):
        q = OperationalQuantities()
        assert q.get_irradiation_angles('h_prime_07') == [0, 15, 30, 45, 60, 75, 90, 180]
        assert q.get_irradiation_angles('h_prime_3') == [0, 15, 30, 45, 60, 75, 90, 180]
        assert q.get_irradiation_angles('h_star_10') == [0]
        assert q.get_irradiation_angles('H_p_07_rod') == [0]
        assert q.get_irradiation_angles('H_p_07_pill') == [0]
        assert q.get_irradiation_angles('H_p_07_slab') == [0, 15, 30, 45, 60, 75]
        assert q.get_irradiation_angles('H_p_3_cyl') == [0, 15, 30, 45, 60, 75, 90]
        assert q.get_irradiation_angles('H_p_10_slab') == [0, 15, 30, 45, 60, 75]

    def test_symbol_from_quantities(self):
        q = OperationalQuantities()
        assert q.get_symbol('h_prime_07') == "H'(0.07)"
        assert q.get_symbol('h_prime_3') == "H'(3)"
        assert q.get_symbol('h_star_10') == "H*(10)"
        assert q.get_symbol('H_p_07_rod') == "Hp(0.07, rod)"
        assert q.get_symbol('H_p_07_pill') == "Hp(0.07, pillar)"
        assert q.get_symbol('H_p_07_slab') == "Hp(0.07, slab)"
        assert q.get_symbol('H_p_3_cyl') == "Hp(3, cyl)"
        assert q.get_symbol('H_p_10_slab') == "Hp(10, slab)"
