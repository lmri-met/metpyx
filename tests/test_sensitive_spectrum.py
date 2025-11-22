import pytest

from metpyx import SensitiveSpectrum, dict_to_tuple_list

class TestDictToTupleList:

    def test_empty_dict(self):
        result = dict_to_tuple_list({})
        assert result == []

    def test_single_item_dict(self):
        result = dict_to_tuple_list({'Al': 4})
        assert result == [('Al', 4)]

    def test_multiple_items_dict(self):
        result = dict_to_tuple_list({'Al': 4, 'Cu': 0.6, 'Air': 1000})
        assert result == [('Al', 4), ('Cu', 0.6), ('Air', 1000)]

class TestSensitiveSpectrumInitialization:

    def test_quality_only_initialization(self):
        filters = [('Be', 0), ('Pb', 0), ('Sn', 0.0), ('Cu', 0.6), ('Al', 4.0)]
        s = SensitiveSpectrum(quality='N60')
        assert s.quality == 'N60'
        assert s.voltage == 60
        assert s.anode is None
        assert s.filtration == filters

    def test_wrong_quality_only_initialization(self):
        with pytest.raises(ValueError):
            SensitiveSpectrum(quality='foo')

    def test_explicit_initialization(self):
        filters = [('Al', 4), ('Cu', 0.6), ('Air', 1000)]
        s = SensitiveSpectrum(voltage=60, anode=20, filtration=filters)
        assert s.quality is None
        assert s.voltage == 60
        assert s.anode == 20
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
