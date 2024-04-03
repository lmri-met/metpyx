import src.metpyx.ionization_chamber as ic


class TestGetRadiationQualitySeries:
    def test_get_radiation_quality_series(self):
        assert ic.get_radiation_quality_series('N-10') == 'N-series'
        assert ic.get_radiation_quality_series('L-30') == 'L-series'
