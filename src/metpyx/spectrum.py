"""Spectral I/O and container utilities for metpyx.

This module provides lightweight containers and helpers for working with
one-dimensional spectra (energy values and associated quantities such as
fluence or counts) and simple CSV-based I/O.

Primary public API
------------------
read_csv(filepath, columns=None, spectrum=False, **kwargs)
    Read two columns from a CSV file and return a :class:`SpectralQuantity`
    or :class:`Spectrum` instance. ``columns`` may be a pair of column
    names or integer indices. Additional keyword arguments are forwarded to
    :func:`pandas.read_csv`.

SpectralQuantity
    Container for a 1-D spectral quantity. Holds ``energy`` and ``value``
    as 1-D :class:`numpy.ndarray` objects and provides ``to_df`` and
    ``to_csv`` convenience methods for serialization.

Spectrum
    :class:`SpectralQuantity` subclass specialized for fluence spectra.
    Exposes a read-only ``fluence`` property that mirrors :attr:`value` and
    uses different default column labels for output.

Notes
-----
The module performs minimal validation (1-D arrays, matching lengths, and
finite numeric values) when constructing container objects. The I/O
helpers are thin wrappers around pandas and numpy; they are intended for
small-to-moderate sized spectral tables and convenience in examples and
tools.

Examples
--------
>>> from metpyx.spectrum import read_csv, SpectralQuantity, Spectrum
>>> q = SpectralQuantity([1, 2, 3], [10, 20, 30])
>>> df = q.to_df()
>>> s = read_csv('my_spectrum.csv', columns=(0, 1), spectrum=True)
"""

from collections.abc import Sequence

import numpy as np
import pandas as pd


def mean_energy(energy, fluence):  # TODO: Implement, document and test
    """Compute the fluence-weighted mean energy.

    Parameters
    ----------
    energy : array_like
        Sequence of photon energies. The function does not convert inputs;
        they must support element-wise multiplication with ``fluence`` (for
        example, :class:`numpy.ndarray` objects).
    fluence : array_like
        Sequence of fluence values corresponding to ``energy``. Must be
        broadcast-compatible with ``energy`` for element-wise multiplication.

    Returns
    -------
    numpy.floating
        Scalar equal to ``sum(energy * fluence) / sum(fluence)``. The exact
        return type (NumPy scalar or Python float) depends on the input types.

    Raises
    ------
    TypeError, ValueError
        If the inputs are not compatible for element-wise multiplication or
        if NumPy raises an exception during the arithmetic operations.

    Notes
    -----
    - This function performs no conversion (e.g., :func:`numpy.asarray`) or
      validation of inputs; callers should convert/validate as needed.
    - If ``sum(fluence)`` is zero the result will be ``NaN`` and NumPy may
      emit a ``RuntimeWarning`` due to invalid division.

    Examples
    --------
    >>> mean_energy(np.array([1, 2, 3]), np.array([10, 20, 30]))
    2.3333333333333335
    """
    return np.divide(np.sum(fluence * energy), np.sum(fluence))


def read_csv(filepath, columns=None, spectrum=False, **kwargs):
    """Read a two-column CSV into a SpectralQuantity or Spectrum.

    Parameters
    ----------
    filepath : str or path-like
        Path to a CSV file. This is passed directly to ``pandas.read_csv``
        along with any additional ``**kwargs``.
    columns : sequence of (str or int), optional
        Two-element sequence selecting the energy and value columns. When
        provided as strings, they are interpreted as column names; when
        provided as integers they are interpreted as column indices (0-based).
        Default is ``(0, 1)`` (first and second columns).
    spectrum : bool, optional
        If True, return a :class:`Spectrum` instance (with attribute
        ``fluence``). Otherwise, return a :class:`SpectralQuantity`.
        Default is False.
    **kwargs
        Extra keyword arguments forwarded to ``pandas.read_csv`` (for example
        ``sep``, ``header``, ``encoding``).

    Returns
    -------
    SpectralQuantity or Spectrum
        An object containing ``energy`` and ``value`` arrays (or ``fluence``
        for Spectrum) as 1-D :class:`numpy.ndarray` of dtype float.

    Raises
    ------
    ValueError
        If ``columns`` is not a two-element sequence of str or int, or if the
        parsed arrays are not 1-D, have mismatched lengths, or contain
        non-finite values.

    Notes
    -----
    The function converts the selected columns to floating-point numpy
    arrays and validates their shape and finiteness. Use the returned
    object's ``to_df`` / ``to_csv`` methods to serialize the spectrum back
    to disk.

    Examples
    --------
    >>> read_csv("data.csv")
    >>> read_csv("data.csv", columns=("E_keV", "fluence"), spectrum=True)
    """
    df = pd.read_csv(filepath, **kwargs)

    if columns is None:
        columns = (0, 1)

    if isinstance(columns, Sequence) and len(columns) == 2:
        if all(isinstance(x, str) for x in columns):
            energy = df[columns[0]].values
            value = df[columns[1]].values
        elif all(isinstance(x, int) for x in columns):
            energy = df.iloc[:, columns[0]].values
            value = df.iloc[:, columns[1]].values
        else:  # TODO: test
            raise ValueError("Columns must be a two-element sequence of str or int")
    else:  # TODO: test
        raise ValueError("Columns must be a two-element sequence of str or int")

    if spectrum:
        return Spectrum(energy, value)
    else:
        return SpectralQuantity(energy, value)


class SpectralQuantity:
    """Container for a 1-D spectral quantity (energy and associated values).

    Parameters
    ----------
    energy : array_like
        1-D sequence of energy values. Converted to a 1-D :class:`numpy.ndarray`
        of dtype float.
    value : array_like
        1-D sequence of values associated with each energy (for example
        counts, intensity, fluence). Converted to a 1-D :class:`numpy.ndarray`
        of dtype float.

    Attributes
    ----------
    energy : numpy.ndarray
        1-D float array of energies.
    value : numpy.ndarray
        1-D float array of values corresponding to each energy.

    Raises
    ------
    ValueError
        If `energy` or `value` is not 1-D, if their lengths differ, or if
        either contains non-finite values (NaN or Inf).

    Notes
    -----
    This class is a lightweight container that performs basic validation on
    initialization and provides convenience methods ``to_df`` and ``to_csv``
    for serialization. Subclasses (such as :class:`Spectrum`) may add
    semantic aliases (for example, ``fluence``) or additional behaviour.

    Examples
    --------
    >>> from metpyx.spectrum import SpectralQuantity
    >>> q = SpectralQuantity([1, 2, 3], [10, 20, 30])
    >>> q.energy
    array([1., 2., 3.])
    """
    DEFAULT_LABELS = ('Energy', 'Value')

    def __init__(self, energy, value):
        """Initialize a SpectralQuantity instance.

        Parameters
        ----------
        energy : array_like
            1-D sequence of energy values. Converted to a 1-D
            :class:`numpy.ndarray` of dtype float.
        value : array_like
            1-D sequence of values associated with each energy (for example
            counts, intensity, or fluence). Converted to a 1-D
            :class:`numpy.ndarray` of dtype float.

        Raises
        ------
        ValueError
            If `energy` or `value` is not 1-D, their lengths differ, or if
            either contains non-finite values (NaN or Inf).

        Examples
        --------
        >>> SpectralQuantity([1, 2, 3], [10, 20, 30])
        """
        energy = np.asarray(energy, dtype=float)
        value = np.asarray(value, dtype=float)

        if energy.ndim != 1 or value.ndim != 1:
            raise ValueError("Energy and value must be 1-D arrays")
        if energy.shape[0] != value.shape[0]:
            raise ValueError("Energy and value must have the same length")
        if not np.isfinite(energy).all() or not np.isfinite(value).all():
            raise ValueError("Energy and value must contain finite numeric values")

        self.energy = energy
        self.value = value

    def to_df(self, labels=DEFAULT_LABELS):
        """Convert the spectral quantity to a pandas DataFrame.

        Parameters
        ----------
        labels : sequence of str, optional
            Two labels for the output DataFrame columns (energy, value).
            By default, this uses :attr:`DEFAULT_LABELS` ("Energy", "Value").

        Returns
        -------
        pandas.DataFrame
            DataFrame with two columns: the first column contains energy
            values and the second contains the associated values.

        Notes
        -----
        The returned DataFrame is created from the underlying numpy arrays
        and does not modify the instance. Use ``to_csv`` on the returned
        DataFrame or on the object to serialize to disk.

        Examples
        --------
        >>> q = SpectralQuantity([1, 2, 3], [10, 20, 30])
        >>> q.to_df()
           Energy  Value
        0     1.0   10.0
        1     2.0   20.0
        2     3.0   30.0
        """
        return pd.DataFrame({labels[0]: self.energy, labels[1]: self.value})

    def to_csv(self, filepath, **kwargs):
        """Serialize the spectral quantity to CSV using pandas.

        Parameters
        ----------
        filepath : str, path-like, file-like or None
            File path or buffer to write the CSV to. If ``None``, the CSV
            representation is returned as a string instead of being written to
            disk. This argument is forwarded to :meth:`pandas.DataFrame.to_csv`.
        **kwargs
            Additional keyword arguments forwarded to
            :meth:`pandas.DataFrame.to_csv` (for example ``sep``, ``index``,
            ``encoding``).

        Returns
        -------
        str or None
            If ``filepath`` is ``None``, returns the CSV text as a string.
            Otherwise, returns ``None`` and writes the CSV to the provided
            path/buffer (behavior mirrors :meth:`pandas.DataFrame.to_csv`).

        Notes
        -----
        This method constructs a :class:`pandas.DataFrame` from the instance
        via ``to_df`` and delegates serialization to pandas. If you need to
        adjust column labels or perform DataFrame-level operations prior to
        writing, call ``to_df`` and operate on the DataFrame directly.

        Examples
        --------
        >>> q = SpectralQuantity([1, 2, 3], [10, 20, 30])
        >>> q.to_csv('out.csv')  # writes to file
        >>> csv_text = q.to_csv(None)  # returns CSV string
        """
        df = self.to_df()
        return df.to_csv(filepath, **kwargs)


class Spectrum(SpectralQuantity):
    """SpectralQuantity specialized for fluence spectra.

    This subclass provides a semantic alias ``fluence`` for the underlying
    ``value`` array and uses different default labels for serialization.

    The ``fluence`` attribute is exposed as a read-only property that
    returns the underlying :attr:`value` array. It is initialized by the
    constructor. To change fluence after construction, assign to
    :attr:`value` explicitly (the property does not support assignment).

    Parameters
    ----------
    energy : array_like
        1-D sequence of energy values (will be converted to a 1-D
        :class:`numpy.ndarray` of dtype float).
    fluence : array_like
        1-D sequence of fluence values corresponding to each energy (will
        be converted to a 1-D :class:`numpy.ndarray` of dtype float).

    Attributes
    ----------
    energy : numpy.ndarray
        1-D float array of energies (inherited from :class:`SpectralQuantity`).
    value : numpy.ndarray
        1-D float array of fluence values corresponding to each energy (inherited from
        :class:`SpectralQuantity`).
    value : numpy.ndarray
        1-D float array of fluence values corresponding to each energy (same object as
        :attr:`value`).

    Notes
    -----
    Validation (1-D, matching lengths, finiteness) is performed by the
    base :class:`SpectralQuantity` during construction. The property
    ``fluence`` returns the current ``value`` array but cannot be assigned
    to directly.

    Examples
    --------
    >>> s = Spectrum([1, 2, 3], [0.1, 0.2, 0.3])
    >>> s.energy
    array([1., 2., 3.])
    >>> s.fluence
    array([0.1, 0.2, 0.3])
    """
    DEFAULT_LABELS = ('Energy', 'Fluence')

    def __init__(self, energy, fluence):
        """Initialize a :class:`Spectrum` instance.

        The constructor delegates validation and array conversion to
        :class:`SpectralQuantity` and does not create independent copies of
        the data. After construction, :attr:`fluence` and :attr:`value`
        reference the same underlying data.

        Parameters
        ----------
        energy : array_like
            1-D sequence of energy values.
        fluence : array_like
            1-D sequence of fluence values.

        Raises
        ------
        ValueError
            If the inputs fail validation performed by
            :class:`SpectralQuantity` (non-1D, mismatched lengths, or
            non-finite values).
        """
        super().__init__(energy, fluence)
        self.fluence = self.value
        delattr(self, "value")

    def get_mean_energy(self):
        """Compute the fluence-weighted mean energy of the spectrum.

        Returns
        -------
        numpy.floating
            Scalar equal to ``sum(energy * fluence) / sum(fluence)``. The exact
            return type (NumPy scalar or Python float) depends on the input types.

        Notes
        -----
        - If ``sum(fluence)`` is zero the result will be ``NaN`` and NumPy may
          emit a ``RuntimeWarning`` due to invalid division.

        Examples
        --------
        >>> s = Spectrum([1, 2, 3], [10, 20, 30])
        >>> s.get_mean_energy()
        2.3333333333333335
        """
        return mean_energy(self.energy, self.fluence)
