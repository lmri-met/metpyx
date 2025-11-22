import metpyx.data as dt


class XrayQuantities:
    """
    A class to represent and manage X-ray related quantities.

    Attributes:
    -----------
    operational_quantities : list
        A list of the operational quantities for x-rays.

    Methods:
    --------
    is_quantity(quantity):
        Checks if the given quantity is an operational quantity for x-rays.
    get_irradiation_angles(quantity):
        Retrieves the irradiation angles for the given operational quantity.
    """

    def __init__(self):
        """
        Initializes an XrayQuantities object with operational quantities.
        """
        self.operational_quantities = dt.OPERATIONAL_QUANTITIES

    def is_quantity(self, quantity):
        """
        Checks if the given quantity is an operational quantity for x-rays.

        Args:
            quantity (str): The quantity to be checked.

        Returns:
            bool: True if the quantity is an operational quantity for x-rays, otherwise False.
        """
        if quantity in self.operational_quantities:
            return True
        else:
            return False

    def get_irradiation_angles(self, quantity):
        """
        Retrieves the irradiation angles for the given operational quantity.

        Args:
            quantity (str): The operational quantity whose irradiation angles are to be retrieved.

        Returns:
            list: The list of irradiation angles corresponding to the given operational quantity.

        Raises:
            ValueError: If the quantity is not an x-ray operational quantity.
        """
        if self.is_quantity(quantity):
            return dt.IRRADIATION_ANGLES[quantity]
        else:
            raise ValueError(f'{quantity} is not an x-ray operational quantity.')
