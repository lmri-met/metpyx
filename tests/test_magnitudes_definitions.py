import src.metpyx.magnitude_definitions as md


class TestMagnitudesDefinitions:
    def test_get_environmental_correction(self):
        # Test case 1: Temperature and pressure equal to reference values
        assert md.get_environmental_correction(298.15, 101325, 298.15, 101325) == 1.0
        # Test case 2: Temperature half of reference value
        assert md.get_environmental_correction(298.15 / 2, 101325, 298.15, 101325) == 0.5
        # Test case 3: Pressure half of reference value
        assert md.get_environmental_correction(298.15, 101325 / 2, 298.15, 101325) == 2.0

    def test_get_current_without_background_and_close_detector(self):
        # Test case without background and close detector
        assert md.get_current(time=10, charge=5) == 0.5

    def test_get_current_with_background_and_close_detector(self):
        # Test case with background and close detector
        assert md.get_current(time=10, charge=5, background=0.1) == 0.4

    def test_get_current_without_background_and_open_detector(self):
        # Test case without background and open detector
        assert md.get_current(time=10, charge=5, open_detector=True, temperature=298.15 / 2, pressure=101325,
                              reference_temperature=298.15, reference_pressure=101325) == 0.25

    def test_get_current_with_background_and_open_detector(self):
        # Test case with background and open detector
        assert md.get_current(time=10, charge=5, background=0.1, open_detector=True, temperature=298.15 / 2,
                              pressure=101325, reference_temperature=298.15, reference_pressure=101325) == 0.2

    def test_get_kerma_rate(self):
        # Test case 1: Positive current
        assert md.get_kerma_rate(current=0.5, calibration_coefficient=0.1, calibration_coefficients_correction=1.2,
                                 distance_factor=2.0) == 0.5 * 0.1 * 1.2 * 2.0
        # Test case 2: Negative current
        assert md.get_kerma_rate(current=-0.5, calibration_coefficient=0.1, calibration_coefficients_correction=1.2,
                                 distance_factor=2.0) == -0.5 * 0.1 * 1.2 * 2.0

    def test_get_operational_magnitude_rate(self):
        # Test case 1: All parameters provided
        assert md.get_operational_magnitude_rate(kerma_rate=0.5, conversion_coefficient=0.1,
                                                 electrometer_range_correction=1.2,
                                                 air_density_correction=2.0) == 0.5 * 0.1 * 1.2 * 2.0

    def test_get_integral_operational_magnitude(self):
        # Test case 1: Positive operational magnitude rate and integration time
        assert md.get_integral_magnitude(magnitude_rate=0.5, integration_time=10) == 0.5 * 10
