import importlib.resources as resources

import pandas as pd

from metpyx.xdata import OperationalQuantities


class Coefficients:
    """
    Loader for coefficient tables with configuration stored as class constants.

    Class attributes
    ----------
    MU_TR : dict
        Configuration for mu_tr/ρ tables (package, default source, and sources config).
    H_K : dict
        Configuration for h_K tables (package, default source, and sources config).

    Attributes
    ----------
    quantities : OperationalQuantities
        OperationalQuantities instance used for validation.
    """

    MU_TR = {
        "pkg": "metpyx.xdata.tables.mu_tr_over_rho_air",
        "default": "pene_2018",
        "sources": {
            "pene_2018": {
                'file': "pene_2018.csv",
                "energy_col": "Energy (keV)",
                "value_col": "μtr/ρ (cm2/g)"
            }
        }
    }
    H_K = {
        "pkg": "metpyx.xdata.tables.h_k",
        "default": "cmi_2025",
        "sources": {
            "cmi_2025": {
                "subdir": "cmi_2025",
                "energy_col": "E keV",
                # value_col depends on angle: f"hK {angle} Sv/Gy"
            }
        }
    }

    def __init__(self):
        """
        Initialize Coefficients.

        Initializes the OperationalQuantities instance used for validation.
        """
        self.quantities = OperationalQuantities()

    @staticmethod
    def get_from_data(pkg, file_or_parts, energy_col, value_col):
        """
        Load coefficient data from package resources.

        Parameters
        ----------
        pkg : str
            Package name containing the data files.
        file_or_parts : str or sequence
            File name or sequence of path parts inside the package.
        energy_col : str
            Column name for energy values in the CSV.
        value_col : str
            Column name for coefficient values in the CSV.

        Returns
        -------
        tuple[numpy.ndarray, numpy.ndarray]
            Tuple of (energies, values) as NumPy arrays.

        Raises
        ------
        FileNotFoundError
            If the requested resource cannot be loaded or parsed.
        """
        try:
            if isinstance(file_or_parts, (list, tuple)):
                data_file = resources.files(pkg).joinpath(*file_or_parts)
            else:
                data_file = resources.files(pkg).joinpath(file_or_parts)
            with data_file.open("r", encoding="utf-8") as fh:
                df = pd.read_csv(fh)
        except Exception as exc:
            raise FileNotFoundError(f"Could not load '{file_or_parts}' from package data:\n{exc}") from exc

        energies = df[energy_col].to_numpy()
        values = df[value_col].to_numpy()
        return energies, values

    def get_mu_tr_over_rho_air(self, source=None):
        """
        Retrieve mass energy transfer coefficients to air (keV, cm²/g).

        Parameters
        ----------
        source : str, optional
            Source key from MU_TR sources or `'custom'`. Defaults to the configured default.

        Returns
        -------
        tuple[numpy.ndarray, numpy.ndarray]
            Tuple of (energies, values) as NumPy arrays.

        Raises
        ------
        ValueError
            If `source` is invalid.
        """
        # Set default source if none provided
        source = self.MU_TR["default"] if source is None else source

        # If source is in predefined sources, load from package data
        if source in self.MU_TR["sources"].keys():

            # Get configuration for the selected source
            pkg = self.MU_TR['pkg']
            file = self.MU_TR["sources"][source]['file']
            energy_col = self.MU_TR["sources"][source]['energy_col']
            value_col = self.MU_TR["sources"][source]['value_col']

            # Load data
            energies, values = self.get_from_data(pkg, file, energy_col, value_col)

        # Invalid source
        else:
            allowed = list(self.MU_TR["sources"].keys())
            raise ValueError(f"Source must be one of {allowed}. Found: {source}")

        return energies, values

    def get_h_k(self, quantity, angle, source=None):
        """
        Retrieve air kerma to dose conversion coefficients (keV, Sv/Gy).

        Parameters
        ----------
        quantity : str
            Operational quantity name required for predefined sources.
        angle : int or float
            Angle in degrees required for predefined sources.
        source : str, optional
            Source key from H_K sources or `'custom'`. Defaults to the configured default.

        Returns
        -------
        tuple[numpy.ndarray, numpy.ndarray]
            Tuple of (energies, values) as NumPy arrays.

        Raises
        ------
        ValueError
            If the requested quantity/angle is invalid for predefined sources.
        """
        # Set default source if none provided
        source = self.H_K["default"] if source is None else source

        # If source is in predefined sources, load from package data
        if source in self.H_K["sources"]:

            # Validate quantity and angle
            if not self.quantities.is_quantity_angle(quantity, angle):
                raise ValueError(f"Quantity {quantity} at {angle} degrees is not in predefined operational quantities.")

            # Get configuration for the selected source
            pkg = self.H_K['pkg']
            subdir = self.H_K["sources"][source]['subdir']
            energy_col = self.H_K["sources"][source]['energy_col']

            # Construct file path and value column
            file_path_parts = (subdir, f"{quantity}.csv")
            value_col = f'hK {angle} Sv/Gy'

            # Load data
            energies, values = self.get_from_data(pkg, file_path_parts, energy_col, value_col)

        # Invalid source
        else:
            allowed = list(self.H_K["sources"].keys())
            raise ValueError(f"Source must be one of {allowed}. Found: {source}")

        return energies, values
