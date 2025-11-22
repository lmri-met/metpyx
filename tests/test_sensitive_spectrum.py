import pytest

from metpyx import SensitiveSpectrum


class TestSensitiveSpectrumInitialization:

    def test_quality_only_initialization(self):
        s = SensitiveSpectrum(quality='N60')
        assert s.quality == 'N60'
        assert s.high_voltage is None
        assert s.anode_angle is None
        assert s.filtration is None

    def test_explicit_initialization(self):
        filters = [('Al', 4), ('Cu', 0.6), ('Air', 1000)]
        s = SensitiveSpectrum(voltage=60, anode=20, filtration=filters)
        assert s.quality is None
        assert s.high_voltage == 60
        assert s.anode_angle == 20
        assert s.filtration == filters

    def test_empty_initialization_raises(self):
        with pytest.raises(ValueError):
            SensitiveSpectrum()

    def test_conflicting_initialization_raises(self):
        with pytest.raises(ValueError):
            SensitiveSpectrum(quality='N60', voltage=60, anode=20, filtration=[('Al', 4)])

    def test_incomplete_explicit_initialization(self):
        with pytest.raises(ValueError):
            SensitiveSpectrum(voltage=60)
