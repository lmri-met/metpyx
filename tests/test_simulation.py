"""Tests for metpyx.simulation

Unit tests for the :mod:`metpyx.simulation` module, focused on the
`SimulatedSpectrum` helper which constructs spectra via :mod:`spekpy`.

The tests in this module exercise the supported initialization modes
(quality-based lookup and explicit voltage-based construction), error
handling for invalid or conflicting arguments, and the correct forwarding
of spectral arrays from :mod:`spekpy` into :class:`metpyx.spectrum.Spectrum`.

Notes
-----
- These tests rely on the external package :mod:`spekpy` to construct
  reference spectra. In CI environments you may prefer to monkeypatch
  or stub :mod:`spekpy` to avoid coupling to the external library.
- Each test is intentionally focused and deterministic so failures are
  easy to diagnose.
"""
import numpy as np
import pytest
from spekpy import Spek

import metpyx.simulation as sim


class TestSimulatedSpectrumConstructor:
    """Tests for the constructor behaviour of :class:`metpyx.simulation.SimulatedSpectrum`.

    These tests exercise the supported initialization modes (quality-based
    lookup via :class:`metpyx.data.Qualities` and explicit voltage-based
    construction), error handling for invalid or conflicting arguments,
    and the forwarding of generated spectral arrays from :mod:`spekpy` to
    the constructed :class:`SimulatedSpectrum` instance.

    Notes
    -----
    - The tests use :class:`spekpy.Spek` to construct an expected reference
      spectrum; in CI you may choose to monkeypatch or stub spekpy to
      avoid external dependency instability.
    - Each test focuses on a single behaviour so failures are easy to
      diagnose.
    """

    def test_conflicting_initialization(self):
        """Raise ValueError for missing or conflicting initialization args.

        Verifies that attempting to construct a :class:`SimulatedSpectrum`
        without providing a valid initialization mode, or by mixing a
        ``quality`` with explicit parameters (``voltage``/``filtration``),
        raises :class:`ValueError`.
        """
        with pytest.raises(ValueError):
            sim.SimulatedSpectrum()
        with pytest.raises(ValueError):
            sim.SimulatedSpectrum(quality="N60", voltage=60)
        with pytest.raises(ValueError):
            sim.SimulatedSpectrum(quality="N60", filtration=[('Be', 1), ('Al', 4)])

    def test_quality_initialization_invalid_quantities(self):
        """Invalid quality identifiers and parameter types raise exceptions.

        - Unknown quality identifiers should raise :class:`ValueError`.
        - Invalid types for parameters (e.g., non-numeric ``voltage``)
          should raise :class:`TypeError` or similar.
        - Malformed ``filtration`` inputs should raise an exception.
        """
        with pytest.raises(ValueError):
            sim.SimulatedSpectrum(quality="INVALID")
        with pytest.raises(ValueError):
            sim.SimulatedSpectrum(quality="INVALID", anode="INVALID")
        with pytest.raises(TypeError):
            sim.SimulatedSpectrum(voltage="INVALID")
        with pytest.raises(Exception):
            sim.SimulatedSpectrum(voltage=30, filtration="INVALID")

    def test_quality_initialization(self):
        """Quality-based initialization returns expected spectral data.

        Constructs a :class:`SimulatedSpectrum` using a named quality and an
        explicitly provided ``anode``. The test builds a reference
        :class:`spekpy.Spek` instance with the same parameters and
        ``multi_filter`` settings, then asserts that the constructed
        object's metadata (``quality``, ``voltage``, ``anode``,
        ``filtration``) and spectral arrays (``energy``, ``fluence``)
        match the reference.
        """
        result = sim.SimulatedSpectrum(quality="N30", anode=20)
        s = Spek(30, 20)
        s.multi_filter([('Be', 1), ('Al', 4)])
        expected_energy, expected_fluence = s.get_spectrum()
        assert result.quality == "N30"
        assert result.voltage == 30
        assert result.anode == 20
        assert result.filtration == [('Be', 1), ('Al', 4)]
        assert isinstance(result.energy, np.ndarray)
        assert isinstance(result.fluence, np.ndarray)
        assert np.allclose(result.energy, expected_energy)
        assert np.allclose(result.fluence, expected_fluence)

    def test_voltage_initialization(self):
        """Explicit voltage initialization produces the correct spectrum.

        When constructed with explicit ``voltage`` and ``anode`` (without
        ``filtration``) the resulting :class:`SimulatedSpectrum` should
        produce the same spectral arrays as a direct :class:`spekpy.Spek`
        instance constructed with the same parameters.
        """
        result = sim.SimulatedSpectrum(voltage=30, anode=20)
        s = Spek(30, 20)
        expected_energy, expected_fluence = s.get_spectrum()
        assert result.quality is None
        assert result.voltage == 30
        assert result.anode == 20
        assert result.filtration is None
        assert isinstance(result.energy, np.ndarray)
        assert isinstance(result.fluence, np.ndarray)
        assert np.allclose(result.energy, expected_energy)
        assert np.allclose(result.fluence, expected_fluence)

    def test_voltage_filtration_initialization(self):
        """Voltage+filtration initialization applies filters and matches spekpy.

        Constructing with explicit ``voltage``, ``anode`` and ``filtration``
        should result in a :class:`SimulatedSpectrum` whose spectral arrays
        match those produced by calling ``multi_filter`` on a
        :class:`spekpy.Spek` instance with the same filtration.
        """
        result = sim.SimulatedSpectrum(voltage=30, anode=20, filtration=[('Be', 1), ('Al', 4)])
        s = Spek(30, 20)
        s.multi_filter([('Be', 1), ('Al', 4)])
        expected_energy, expected_fluence = s.get_spectrum()
        assert result.quality is None
        assert result.voltage == 30
        assert result.anode == 20
        assert result.filtration == [('Be', 1), ('Al', 4)]
        assert isinstance(result.energy, np.ndarray)
        assert isinstance(result.fluence, np.ndarray)
        assert np.allclose(result.energy, expected_energy)
        assert np.allclose(result.fluence, expected_fluence)
