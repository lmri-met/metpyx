class Densities:
    _RHO = {
        "nist": {
            # https://physics.nist.gov/PhysRefData/XrayMassCoef/tab1.html
            "source": "NIST",
            "unit": "g/cm3",
            "values": {
                "Al": 2.699,
                "Cu": 8.960,
                "Sn": 7.310,
                "Pb": 11.35,
                "Fe": 7.874,
                "Si": 2.330,
                "S": 2.000,
                "O": 0.001332,
                "Ni": 8.902,
                "Sb": 6.691,
                "Bi": 9.747,
            }
        }
    }

    def get_density(self, material, source="nist"):
        """
        Retrieve the density of a material in g/cm³.

        Parameters
        ----------
        material : str
            Material symbol (e.g., 'Al', 'Cu', 'Sn', etc.).
        source : str, optional
            Source of density values. Defaults to 'nist'.

        Returns
        -------
        float
            Density of the material in g/cm³.

        Raises
        ------
        ValueError
            If the material is not found in the density data or if the source is invalid.
        """
        if source not in self._RHO:
            allowed = list(self._RHO.keys())
            raise ValueError(f"Source must be one of {allowed}. Found: {source}")

        try:
            return self._RHO[source]["values"][material]
        except KeyError as exc:
            raise ValueError(f"Material '{material}' not found in densities source.") from exc
