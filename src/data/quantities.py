class OperationalQuantities:
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
        self.operational_quantities = dict(self._OPERATIONAL_QUANTITIES)

    def get_all_quantities(self, symbol=False):
        if symbol:
            return [quantity['symbol'] for quantity in self.operational_quantities.values()]
        else:
            return list(self.operational_quantities.keys())

    def is_quantity(self, quantity):
        return quantity in self.operational_quantities

    def is_quantity_angle(self, quantity, angle):
        if self.is_quantity(quantity) and angle in self.operational_quantities[quantity]['angles']:
            return True
        else:
            return False

    def get_quantity(self, quantity):
        if self.is_quantity(quantity):
            return self.operational_quantities[quantity]
        else:
            raise ValueError(f'{quantity} is not an x-ray operational quantity.')

    def get_irradiation_angles(self, quantity):
        q = self.get_quantity(quantity)
        return q['angles']

    def get_symbol(self, quantity):
        q = self.get_quantity(quantity)
        return q['symbol']
