import importlib.resources as resources

import pandas as pd

from metpyx.data import OperationalQuantities


class Coefficients:
    """
    Loader for coefficient tables with configuration stored as class constants.

    Class constants:
    - MU_TR: configuration for mu_tr/ρ tables.
    - H_K: configuration for h_K tables.

    Instance attributes:
    - quantities: OperationalQuantities instance used for validation.
    - mu_tr_source: selected default source for mu_tr/ρ.
    - h_k_source: selected default source for h_K.
    """

    MU_TR = {
        "pkg": "metpyx.data.tables.mu_tr_over_rho_air",
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
        "pkg": "metpyx.data.tables.h_k",
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
        self.quantities = OperationalQuantities()

    @staticmethod
    def get_from_data(pkg, file_or_parts, energy_col, value_col):
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

    @staticmethod
    def get_from_user(file_path, energy_col, value_col):
        try:
            df = pd.read_csv(file_path, encoding="utf-8")
        except Exception as exc:
            raise FileNotFoundError(f"Could not load '{file_path}':\n{exc}") from exc

        energies = df[energy_col].to_numpy()
        values = df[value_col].to_numpy()
        return energies, values

    def get_mu_tr_over_rho_air(self, source=None, file_path=None, energy_col=None, value_col=None):
        """
        Retrieve mass energy transfer coefficients to air (keV, cm²/g).
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

        # If source is 'custom', load data from user file
        elif source == 'custom':

            # Validate required parameters
            if file_path is None or energy_col is None or value_col is None:
                raise ValueError("For 'custom' source, file_path, energy_col, and value_col must be provided.")

            # Load data
            energies, values = self.get_from_user(file_path, energy_col, value_col)

        # Invalid source
        else:
            allowed = list(self.MU_TR["sources"].keys())
            raise ValueError(f"Source must be one of {allowed} or 'custom'. Found: {source}")

        return energies, values

    def get_h_k(self, source=None, quantity=None, angle=None, file_path=None, energy_col=None, value_col=None):
        """
        Retrieve air kerma to dose conversion coefficients (keV, Sv/Gy).
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

        # If source is 'custom', load data from user file
        elif source == 'custom':

            # Validate required parameters
            if file_path is None or energy_col is None or value_col is None:
                raise ValueError("For 'custom' source, file_path, energy_col, and value_col must be provided.")

            # Load data
            energies, values = self.get_from_user(file_path, energy_col, value_col)

        # Invalid source
        else:
            allowed = list(self.H_K["sources"].keys())
            raise ValueError(f"Source must be one of {allowed} or 'custom'. Found: {source}")

        return energies, values
