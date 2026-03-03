import pytest

from metpyx.uspekpy.sensitivity import PerturbedQuality


class TestQualitySensitivityInvalidInputs:
    def test_constructor_invalid_perturbation_parameter(self):
        with pytest.raises(ValueError) as exc_info:
            PerturbedQuality("N60", 'invalid_parameter', 5, material='Pb', th=20)
        assert f"Unsupported parameter: 'invalid_parameter'" in str(exc_info.value)

    def test_constructor_not_provided_purity_material(self):
        with pytest.raises(ValueError) as exc_info:
            PerturbedQuality("N60", 'additional_filtration_purity', 5, th=20)
        assert f"Material must be specified for 'additional_filtration_purity'" in str(exc_info.value)
