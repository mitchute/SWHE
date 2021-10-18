from typing import Union

from CoolProp.CoolProp import PropsSI


class Fluid(object):
    def __init__(self, data: dict):
        self.concentration = None
        self.fluid_str = None
        if "concentration" in data:
            self.init_fluid(fluid_str=data["fluid"], concentration=data["concentration"])
        else:
            self.init_fluid(fluid_str=data["fluid"])

    @staticmethod
    def get_valid_fluid_str(fluid_key: str, concentration: Union[int, float] = None):
        """
        Get a valid fluid string
        :param fluid_key: fluid key
        :param concentration: concentration, 0-60, optional argument (for water)
        :return: valid fluid string
        """

        if concentration is None:
            valid_fluids = {
                "WATER": "WATER",
                "PG": f"INCOMP::MPG",
                "EG": f"INCOMP::MEG",
                "EA": f"INCOMP::MEA",
            }
        else:
            valid_fluids = {
                "WATER": "WATER",
                "PG": f"INCOMP::MPG[{concentration:0.3f}]",
                "EG": f"INCOMP::MEG[{concentration:0.3f}]",
                "EA": f"INCOMP::MEA[{concentration:0.3f}]",
            }

        return valid_fluids[fluid_key.upper()]

    def init_fluid(self, fluid_str: str, concentration: Union[int, float] = None):
        """
        Initialize the fluid object
        :param fluid_str: fluid string choice
                          "Water", "PG" (Propylene Glycol), "EG" (Ethylene Glycol), "EA" (Ethyl Alcohol)
        :param concentration: volumetric concentration, 0-60, optional argument (for water)
        :return: None
        """

        if fluid_str.upper() != "WATER":
            self.concentration = concentration / 100.0
            self.fluid_str = self.get_valid_fluid_str(fluid_str, self.concentration)
        else:
            self.fluid_str = self.get_valid_fluid_str(fluid_str)

    @staticmethod
    def c_to_k(temp_in_c: Union[int, float]):
        """
        Convert Celsius to Kelvin
        :param temp_in_c: temperature, [C]
        :return: temperature, [K]
        """
        return temp_in_c + 273.15

    def density(self, temperature: Union[int, float]):
        """
        Calculates the fluid density
        :param temperature: temperature, [C]
        :return: density, [kg/m^3]
        """
        return PropsSI("D", "T", self.c_to_k(temperature), "P", 101325, self.fluid_str)

    def specific_heat(self, temperature: Union[int, float]):
        """
        Calculates the fluid specific heat
        :param temperature: temperature, [C]
        :return: specific heat, [J/kg-K]
        """
        return PropsSI("C", "T", self.c_to_k(temperature), "P", 101325, self.fluid_str)

    def viscosity(self, temperature: Union[int, float]):
        """
        Calculates the dynamic viscosity of the fluid
        :param temperature: temperature, [C]
        :return: dynamic viscosity, [Pa-s]
        """
        return PropsSI("VISCOSITY", "T", self.c_to_k(temperature), "P", 101325, self.fluid_str)
