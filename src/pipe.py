from math import log, pi


class Pipe(object):
    def __init__(self, data):
        self.outer_dia = data["outer-dia"]
        self.inner_dia = data["inner-dia"]
        self.thickness = (self.outer_dia - self.inner_dia) / 2.0

        if self.thickness < 0.0:
            msg = f"Inner and outer pipe diameters result in negative pipe thickness\n" \
                  f"Outer dia: {self.outer_dia:0.4f}; Inner dia: {self.inner_dia:0.4f}"
            raise ValueError(msg)

        self.length = data["length"]
        self.density = data["density"]
        self.conductivity = data["conductivity"]

        self.area_cr_inner = None
        self.area_cr_outer = None
        self.area_surf_inner = None
        self.area_surf_outer = None
        self.resist_cond = None
        self.update_pipe()

    def update_pipe(self):
        self.area_cr_inner = self.calc_inner_cross_sectional_area()
        self.area_cr_outer = self.calc_outer_cross_sectional_area()
        self.area_surf_inner = self.calc_inner_surface_area()
        self.area_surf_outer = self.calc_outer_surface_area()
        self.resist_cond = self.calc_cond_resistance()

    def calc_inner_cross_sectional_area(self):
        """
        Calculate the pipe inner cross-sectional area
        :return: inner cross-sectional area, [m^2]
        """
        return (pi / 4.0) * self.inner_dia ** 2

    def calc_outer_cross_sectional_area(self):
        """
        Calculate the pipe outer cross-sectional area
        :return: outer cross-sectional area, [m^2]
        """
        return (pi / 4.0) * self.outer_dia ** 2

    def calc_inner_surface_area(self):
        """
        Calculate the pipe inner surface area
        :return: inner surface area, [m^2]
        """
        return pi * self.inner_dia * self.length

    def calc_outer_surface_area(self):
        """
        Calculate the pipe outer surface area
        :return: outer surface area, [m^2]
        """
        return pi * self.outer_dia * self.length

    def calc_cond_resistance(self):
        """
        Calculate pipe conduction thermal resistance
        :return: resistance, [K/W]
        """
        return log(self.outer_dia / self.inner_dia) / (2 * pi * self.conductivity * self.length)
