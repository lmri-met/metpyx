"""Tests for metpyx.spectrum (NumPy/SciPy-style).

This module contains unit tests for the public behaviours of
:mod:`metpyx.spectrum` including CSV I/O and the lightweight container
classes (:class:`SpectralQuantity`, :class:`Spectrum`). Tests are organized
into classes that group related behaviours:

- ``TestReadCSV``: exercises the ``read_csv`` convenience wrapper (column
  selection by name/index, forwarding pandas kwargs, and error modes).
- ``TestSpectralQuantityConstructor``: validates constructor conversion and
  input validation for :class:`SpectralQuantity` (dtype conversion, shape
  checks, finiteness checks).
- ``TestSpectralQuantityExport``: verifies the ``to_df`` / ``to_csv``
  export helpers and that pandas kwargs are forwarded.
- ``TestSpectrumConstructor``: validates :class:`Spectrum` construction and
  fluence semantics.

Fixtures
--------
Most tests use pytest builtin fixtures:
- ``tmp_path``: for temporary file creation and round-trip CSV checks.

Notes
-----
- Tests import the local package under tests via ``import metpyx.spectrum as sp``.
  When running tests from the project root, set ``PYTHONPATH=src`` so the
  local package is importable (or install the package into the test
  environment).

Examples
--------
Run the full test module from the project root:

    PYTHONPATH=src pytest tests/test_spectrum.py -q

Run a single test class:

    PYTHONPATH=src pytest tests/test_spectrum.py::TestSpectralQuantityConstructor -q
"""

import io

import numpy as np
import pandas as pd
import pytest
import spekpy as spk

import metpyx.spectrum as sp


class TestMeanEnergy:
    """Unit tests for :func:`metpyx.spectrum.mean_energy`.

    This test class verifies the core behaviours of the ``mean_energy``
    helper: correct fluence-weighted mean calculation and handling of a
    zero total fluence.

    Notes
    -----
    Tests use small :mod:`numpy` arrays and rely on :mod:`pytest` helpers
    (``pytest.approx`` and ``pytest.raises``) and :func:`numpy.isnan`
    for numeric assertions.
    """

    def test_value(self):
        """Verify correct fluence-weighted mean is returned.

        Constructs simple ``energy`` and ``fluence`` arrays and asserts that
        the returned scalar equals::

            sum(energy * fluence) / sum(fluence)

        Raises
        ------
        AssertionError
            If the computed value does not approximately equal the expected result.
        """
        energy = np.array([1, 2, 3])
        fluence = np.array([10, 20, 10])
        expected = (1 * 10 + 2 * 20 + 3 * 10) / (10 + 20 + 10)
        result = sp.mean_energy(energy, fluence)
        assert result == pytest.approx(expected)

    def test_zero_total_fluence_returns_nan(self):
        """Return NaN when the total fluence is zero.

        When the ``fluence`` array sums to zero the implementation performs
        a division that yields ``NaN``. This test verifies that behaviour by
        asserting the result is ``numpy.nan``.

        Raises
        ------
        AssertionError
            If the result is not ``NaN``.
        """
        energy = np.array([1, 2, 3])
        fluence = np.array([0, 0, 0])
        result = sp.mean_energy(energy, fluence)
        assert np.isnan(result)


class TestReadCSV:
    """Tests for the CSV-reading helper `read_csv`.

    These tests exercise the :func:`metpyx.spectrum.read_csv` convenience
    wrapper which reads two columns (energy and value/fluence) from a CSV
    and returns either a :class:`metpyx.spectrum.SpectralQuantity` or a
    :class:`metpyx.spectrum.Spectrum` depending on the ``spectrum`` flag.

    Notes
    -----
    All tests create temporary CSV files using the pytest ``tmp_path``
    fixture and verify both the returned type and the numeric contents of
    the ``energy`` and ``value`` arrays.
    """

    @staticmethod
    def _make_csv(path, content):
        """Create a CSV file at ``path / 'spectrum.csv'`` with ``content``.

        Parameters
        ----------
        path : pathlib.Path
            Temporary directory path provided by pytest's ``tmp_path``.
        content : str
            Text content to write to the CSV file.

        Returns
        -------
        pathlib.Path
            Path to the written CSV file.
        """
        # Helper to create a CSV file in a temporary directory
        csv_path = path / "spectrum.csv"
        csv_path.write_text(content)
        return csv_path

    def test_default_reads_first_two_columns(self, tmp_path):
        """Default behaviour: read first two columns as energy and value.

        Given a CSV with three columns (energy, fluence, other) and default
        ``columns`` argument, ``read_csv`` should read the first column as
        ``energy`` and the second as ``value`` and return a
        :class:`metpyx.spectrum.SpectralQuantity`.
        """
        content = "energy,fluence,other\n1,10,100\n2,20,200\n3,30,300\n"
        csv_path = self._make_csv(tmp_path, content)
        result = sp.read_csv(str(csv_path))
        assert isinstance(result, sp.SpectralQuantity)
        assert np.allclose(result.energy, np.array([1, 2, 3]))
        assert np.allclose(result.value, np.array([10, 20, 30]))

    def test_columns_by_name_and_spectrum_true(self, tmp_path):
        """Select columns by name and request a Spectrum instance.

        Given a CSV with named columns, passing ``columns=("energy", "fluence")``
        and ``spectrum=True`` should return a :class:`metpyx.spectrum.Spectrum`
        whose ``energy`` and ``value`` arrays match the CSV content.
        """
        content = "energy,fluence,other\n1,10,100\n2,20,200\n3,30,300\n"
        csv_path = self._make_csv(tmp_path, content)
        result = sp.read_csv(str(csv_path), columns=("energy", "fluence"), spectrum=True)
        assert isinstance(result, sp.Spectrum)
        assert np.allclose(result.energy, np.array([1, 2, 3]))
        assert np.allclose(result.value, np.array([10, 20, 30]))

    def test_columns_by_index(self, tmp_path):
        """Select columns by integer index positions.

        Passing integer indices ``columns=(0, 1)`` should read the first and
        second columns by position and return a :class:`SpectralQuantity`.
        """
        content = "energy,fluence,other\n1,10,100\n2,20,200\n3,30,300\n"
        csv_path = self._make_csv(tmp_path, content)
        result = sp.read_csv(str(csv_path), columns=(0, 1))
        assert isinstance(result, sp.SpectralQuantity)
        assert np.allclose(result.energy, np.array([1, 2, 3]))
        assert np.allclose(result.value, np.array([10, 20, 30]))

    def test_forwards_pandas_kwargs(self, tmp_path):
        """Verify that additional kwargs are forwarded to pandas.read_csv.

        For example, a semicolon-separated file should be read correctly when
        ``sep=';'`` is provided.
        """
        content = "energy;fluence\n1;10\n2;20\n3;30\n"
        csv_path = self._make_csv(tmp_path, content)
        result = sp.read_csv(str(csv_path), sep=";")
        assert isinstance(result, sp.SpectralQuantity)
        assert np.allclose(result.energy, np.array([1, 2, 3]))
        assert np.allclose(result.value, np.array([10, 20, 30]))

    def test_raises_on_invalid_column_spec(self, tmp_path):
        """Raise ValueError when specified columns are invalid.

        If the specified column names or indices do not exist in the CSV,
        ``read_csv`` should raise a :class:`ValueError`.
        """
        content = "energy,fluence\n1,10\n2,20\n3,30\n"
        csv_path = self._make_csv(tmp_path, content)
        with pytest.raises(ValueError):
            sp.read_csv(str(csv_path), columns=(1, 2, 3))
        with pytest.raises(ValueError):
            sp.read_csv(str(csv_path), columns=(1.5, 5.3))
        with pytest.raises(KeyError):
            sp.read_csv(str(csv_path), columns=('invalid', 'name'))
        with pytest.raises(IndexError):
            sp.read_csv(str(csv_path), columns=(0, 5))


class TestSpectralQuantityConstructor:
    """Unit tests for :class:`metpyx.spectrum.SpectralQuantity` constructor.

    These tests validate that the constructor converts inputs to 1-D numpy
    float arrays and raises appropriate errors for invalid inputs such as
    non-1D sequences, mismatched lengths, and non-finite values. The tests
    exercise the validation logic in :meth:`metpyx.spectrum.SpectralQuantity.__init__`.

    Notes
    -----
    - Uses plain Python sequences and numpy values as inputs to ensure
      conversion behavior.
    - Each test focuses on a single failure mode or conversion behavior so
      failures are easy to diagnose.
    """

    def test_converts_inputs_to_numpy_and_dtype_float(self):
        """Inputs are converted to numpy.ndarray with float dtype.

        Given Python sequences for `energy` and `value`, the constructor
        should produce ``energy`` and ``value`` attributes that are
        :class:`numpy.ndarray` instances with floating dtypes and preserved
        numeric contents.
        """
        q = sp.SpectralQuantity([1, 2, 3], (10, 20, 30))
        assert isinstance(q.energy, np.ndarray)
        assert isinstance(q.value, np.ndarray)
        assert np.issubdtype(q.energy.dtype, np.floating)
        assert np.issubdtype(q.value.dtype, np.floating)
        assert np.allclose(q.energy, np.array([1.0, 2.0, 3.0]))
        assert np.allclose(q.value, np.array([10.0, 20.0, 30.0]))

    def test_raises_on_non_1d_inputs(self):
        """Raise ValueError for non-1D input arrays.

        Passing nested sequences (2-D-like) for either `energy` or `value`
        should trigger a :class:`ValueError` because the constructor
        requires 1-D arrays.
        """
        with pytest.raises(ValueError):
            sp.SpectralQuantity([[1, 2], [3, 4]], [1, 2, 3, 4])
        with pytest.raises(ValueError):
            sp.SpectralQuantity([1, 2, 3, 4], [[1, 2], [3, 4]])

    def test_raises_on_mismatched_lengths(self):
        """Raise ValueError when `energy` and `value` lengths differ.

        If the input sequences have different lengths the constructor should
        raise :class:`ValueError` to prevent misaligned spectral data.
        """
        with pytest.raises(ValueError):
            sp.SpectralQuantity([1, 2, 3], [1, 2])

    def test_raises_on_non_finite_values(self):
        """Raise ValueError for arrays containing NaN or Inf.

        The constructor should validate that both arrays contain only finite
        numeric values and raise :class:`ValueError` when NaN or Inf values
        are present.
        """
        with pytest.raises(ValueError):
            sp.SpectralQuantity([1, 2, 3], [1, np.nan, 3])
        with pytest.raises(ValueError):
            sp.SpectralQuantity([1, np.inf, 3], [1, 2, 3])


class TestSpectralQuantityExport:
    """Tests for :class:`metpyx.spectrum.SpectralQuantity` export helpers.

    This test group verifies that :meth:`metpyx.spectrum.SpectralQuantity.to_df`
    and :meth:`metpyx.spectrum.SpectralQuantity.to_csv` produce correct
    outputs under common usage patterns and that optional arguments are
    forwarded to the underlying pandas serialization routines.
    """

    def test_to_df_default_labels(self):
        """to_df produces a DataFrame with the default column labels.

        Ensures the returned :class:`pandas.DataFrame` uses
        :attr:`metpyx.spectrum.SpectralQuantity.DEFAULT_LABELS` for column
        names and that the numeric contents match the underlying arrays.
        """
        q = sp.SpectralQuantity([1, 2, 3], [10, 20, 30])
        df = q.to_df()
        assert isinstance(df, pd.DataFrame)
        assert list(df.columns) == list(sp.SpectralQuantity.DEFAULT_LABELS)
        assert np.allclose(df[sp.SpectralQuantity.DEFAULT_LABELS[0]].values, np.array([1.0, 2.0, 3.0]))
        assert np.allclose(df[sp.SpectralQuantity.DEFAULT_LABELS[1]].values, np.array([10.0, 20.0, 30.0]))

    def test_to_df_custom_labels(self):
        """to_df accepts custom column labels and uses them in the DataFrame.

        Passing a two-element ``labels`` tuple should set the DataFrame column
        names accordingly; the numeric contents should remain unchanged.
        """
        q = sp.SpectralQuantity([1, 2, 3], [10, 20, 30])
        labels = ("E", "V")
        df = q.to_df(labels=labels)
        assert list(df.columns) == list(labels)
        assert np.allclose(df["E"].values, np.array([1.0, 2.0, 3.0]))
        assert np.allclose(df["V"].values, np.array([10.0, 20.0, 30.0]))

    def test_to_csv_writes_file(self, tmp_path):
        """to_csv writes a CSV file when given a file path.

        When provided a filepath the method should write the CSV to disk and
        return ``None`` (pandas' behavior). The written file should contain
        the same numeric data and default labels.

        Parameters
        ----------
        tmp_path : pathlib.Path
            pytest temporary directory fixture used to write the output file.
        """
        q = sp.SpectralQuantity([1, 2, 3], [10, 20, 30])
        out = tmp_path / "out.csv"
        result = q.to_csv(str(out))
        assert result is None
        df = pd.read_csv(out)
        assert np.allclose(df[sp.SpectralQuantity.DEFAULT_LABELS[0]].values, np.array([1.0, 2.0, 3.0]))
        assert np.allclose(df[sp.SpectralQuantity.DEFAULT_LABELS[1]].values, np.array([10.0, 20.0, 30.0]))

    def test_to_csv_returns_string_when_filepath_none(self):
        """to_csv returns CSV text when ``filepath`` is ``None``.

        If ``filepath`` is ``None`` the method should return the CSV
        representation as a string. The returned text should parse to a
        DataFrame that matches the instance data.
        """
        q = sp.SpectralQuantity([1, 2, 3], [10, 20, 30])
        csv_text = q.to_csv(None)
        assert isinstance(csv_text, str)
        df = pd.read_csv(io.StringIO(csv_text))
        assert np.allclose(df[sp.SpectralQuantity.DEFAULT_LABELS[0]].values, np.array([1.0, 2.0, 3.0]))
        assert np.allclose(df[sp.SpectralQuantity.DEFAULT_LABELS[1]].values, np.array([10.0, 20.0, 30.0]))

    def test_to_csv_forwards_pandas_kwargs_sep(self, tmp_path):
        """to_csv forwards keyword arguments to :meth:`pandas.DataFrame.to_csv`.

        For example, providing ``sep=';'`` and ``index=False`` should result
        in a semicolon-separated file without an index column.

        Parameters
        ----------
        tmp_path : pathlib.Path
            pytest temporary directory fixture used to write the output file.
        """
        q = sp.SpectralQuantity([1, 2, 3], [10, 20, 30])
        out = tmp_path / "out_semicolon.csv"
        q.to_csv(str(out), sep=";", index=False)
        df = pd.read_csv(out, sep=";")
        assert np.allclose(df[sp.SpectralQuantity.DEFAULT_LABELS[0]].values, np.array([1.0, 2.0, 3.0]))
        assert np.allclose(df[sp.SpectralQuantity.DEFAULT_LABELS[1]].values, np.array([10.0, 20.0, 30.0]))


class TestSpectrumConstructor:
    """Unit tests for :class:`metpyx.spectrum.Spectrum` constructor.

    These tests validate the behaviour of :class:`metpyx.spectrum.Spectrum` on
    construction. They check that inputs are converted to 1-D floating
    :class:`numpy.ndarray` objects, that the semantic alias ``fluence`` maps
    to the underlying ``value`` array, and that invalid inputs raise
    appropriate :class:`ValueError` exceptions (non-1D inputs, mismatched
    lengths, or non-finite values).

    Notes
    -----
    - Tests use simple Python sequences and numpy scalars to exercise
      conversion and validation logic inherited from
      :class:`metpyx.spectrum.SpectralQuantity`.
    - Keep tests small and focused so failures are easy to interpret.
    """

    def test_converts_inputs_to_numpy_and_dtype_float(self):
        """Construction converts inputs and exposes a fluence alias.

        Given 1-D Python sequences for ``energy`` and ``fluence``, the
        constructor should produce ``energy``, ``value`` and ``fluence``
        attributes that are :class:`numpy.ndarray` instances with floating
        dtype and matching numeric contents. ``fluence`` must be a semantic
        alias of ``value`` (i.e., refer to the same object).
        """
        s = sp.Spectrum([1, 2, 3], (0.1, 0.2, 0.3))
        assert isinstance(s.energy, np.ndarray)
        assert isinstance(s.value, np.ndarray)
        assert isinstance(s.fluence, np.ndarray)
        assert np.issubdtype(s.energy.dtype, np.floating)
        assert np.issubdtype(s.value.dtype, np.floating)
        assert np.issubdtype(s.fluence.dtype, np.floating)
        assert np.allclose(s.energy, np.array([1.0, 2.0, 3.0]))
        assert np.allclose(s.fluence, np.array([0.1, 0.2, 0.3]))
        # fluence should be a semantic alias of value
        assert s.fluence is s.value


class TestSpectrumGetMeanEnergy:
    """Unit tests for :meth:`metpyx.spectrum.Spectrum.get_mean_energy`.

    These tests verify that :meth:`metpyx.spectrum.Spectrum.get_mean_energy`
    computes the same mean energy as the reference implementation in
    :mod:`spekpy` for a representative spectrum. The class uses
    :mod:`spekpy` to generate a test spectrum (energy and fluence) and
    compares the result of the method under test to ``spekpy``'s
    ``get_emean`` result.

    Notes
    -----
    - Requires ``spekpy`` to be importable in the test environment.
    - Tests assert numeric equality/approximate equality; small numeric
      differences may be acceptable but are checked with ``pytest.approx``.
    """

    def test_get_mean_energy(self):
        """Compare :meth:`Spectrum.get_mean_energy` against the spekpy reference.

        The test constructs a ``spekpy.Spek`` instance with typical tube
        parameters, obtains its (energy, fluence) spectrum and reference
        mean energy, wraps the arrays in a
        :class:`metpyx.spectrum.Spectrum`, and verifies that
        ``Spectrum.get_mean_energy()`` returns the expected scalar.

        Raises
        ------
        AssertionError
            If the computed mean energy does not approximately equal the
            spekpy-provided expected value.
        """
        s = spk.Spek(30, 20)
        energy, fluence = s.get_spectrum()
        expected = s.get_emean()

        spectrum = sp.Spectrum(energy, fluence)
        result = spectrum.get_mean_energy()

        assert result == expected
        assert result == pytest.approx(expected)
