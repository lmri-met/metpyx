import pytest
import spekpy as sp

from metpyx.sim.sim import Quality


@pytest.fixture(scope="module")
def quality():
    return Quality("N60")


@pytest.fixture(scope="module")
def spek():
    s = sp.Spek(kvp=60)
    s.multi_filter([["Al", 4.0], ["Cu", 0.6]])
    return s

class TestQualityConsistency:
    def test_attributes(self, quality):
        assert quality.quality == "N60"
        assert quality.voltage == 60
        assert quality.total_filtration == {"Al": 4, "Cu": 0.6}

    def test_spekpy_integral_quantities(self, quality, spek):
        assert quality.get_emean() == spek.get_emean()
        assert quality.get_kerma() == spek.get_kerma()
        assert quality.get_hvl1() == spek.get_hvl1()
        assert quality.get_hvl2() == spek.get_hvl2()
        assert quality.get_hvl1(matl="Cu") == spek.get_hvl1(matl="Cu")
        assert quality.get_hvl2(matl="Cu") == spek.get_hvl2(matl="Cu")