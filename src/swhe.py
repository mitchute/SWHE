from math import exp
from typing import Union

from src.fluid import Fluid
from src.pipe import Pipe
from src.utilities import smoothing_function


class SWHE(object):
    def __init__(self, data):

        # input data
        self.pipe = Pipe(data["pipe"])
        self.brine = Fluid(data["fluid"])
        self.water = Fluid({"fluid-name": "water"})
        self.coil_dia = data["diameter"]
        self.dx = data["horizontal-spacing"]
        self.dy = data["vertical-spacing"]

        # other member data
        self.include_inside_fouling = False
        self.include_outside_fouling = False

    def calc_v_dot(self, m_dot: Union[int, float], temperature: Union[int, float]):
        """
        Calculate volume flow rate
        :param m_dot: mass flow rate, [kg/s]
        :param temperature temperature, [C]
        :return: volume flow rate, [m^3/s]
        """

        return m_dot / self.brine.density(temperature)

    def calc_fluid_velocity(self, m_dot: Union[int, float], temperature: Union[int, float]):
        """
        Calculate mean fluid velocity inside pipe
        :param m_dot: mass flow rate, [kg/s]
        :param temperature: temperature, [C]
        :return: mean fluid velocity, [m/s]
        """

        return self.calc_v_dot(m_dot, temperature) / self.pipe.area_cr_inner

    @staticmethod
    def calc_laminar_nusselt_inside():
        """
        Compute laminar Nusselt number for average of uniform heat flux
        and uniform wall temperature boundary conditions.
        :return: laminar Nusselt no. [-]
        """

        return 4.0

    def calc_turbulent_nusselt_inside(self, reynolds, temperature):
        """
        Compute turbulent Nusselt number using Rogers and Mayhew 1964.
        :param reynolds: Reynolds no., [-]
        :param temperature: temperature, [C]
        :return: turbulent Nusselt no. [-]
        """

        prandtl = self.brine.prandtl(temperature)
        return 0.023 * (reynolds ** 0.85) * (prandtl ** 0.4) * (self.pipe.inner_dia / self.coil_dia) ** 0.1

    def calc_reynolds_no(self, m_dot: Union[int, float], temperature: Union[int, float]):
        """
        Compute Reynolds number
        :param m_dot: mass flow rate, [kg/s]
        :param temperature: temperature, [C]
        :return: Reynolds no. [-]
        """

        density = self.brine.density(temperature)
        dyn_visc = self.brine.viscosity(temperature)
        velocity = self.calc_fluid_velocity(m_dot, temperature)
        return velocity * self.pipe.inner_dia * density / dyn_visc

    def calc_inside_conv_resistance(self, m_dot: Union[int, float], temperature: Union[int, float]):
        """
        Compute inside convection resistance
        :param m_dot: mass flow rate, [kg/s]
        :param temperature: temperature of fluid, [C]
        :return: inside convection resistance, [K/W]
        """

        # compute reynolds no
        reynolds = self.calc_reynolds_no(m_dot, temperature)

        # compute nusselt number
        reynolds_low_cutoff = 500
        reynolds_high_cutoff = 5000
        if reynolds < reynolds_low_cutoff:
            nusselt = self.calc_laminar_nusselt_inside()
        elif reynolds_low_cutoff <= reynolds < reynolds_high_cutoff:
            x = smoothing_function(reynolds, reynolds_low_cutoff, reynolds_high_cutoff, 0, 1)
            nusselt_lam = self.calc_laminar_nusselt_inside()
            nusselt_turb = self.calc_turbulent_nusselt_inside(reynolds, temperature)
            nusselt = nusselt_lam * (1 - x) + nusselt_turb * x
        else:
            nusselt = self.calc_turbulent_nusselt_inside(reynolds, temperature)

        # compute resistance
        cond = self.brine.conductivity(temperature)
        h_in = nusselt * cond / self.pipe.inner_dia
        return 1 / (h_in * self.pipe.area_surf_inner)

    def calc_outside_conv_resistance(self, q_coil: Union[int, float],
                                     temperature: Union[int, float],
                                     temperature_sw: Union[int, float]):
        """
        Computer outside tube resistance
        :param q_coil: coil heat transfer rate, [W]
        :param temperature: brine temperature, [C]
        :param temperature_sw: surface water temperature, [C]
        :return: outside convection resistance, [K/W]
        """

        gravity = 9.81

        # coil heat flux
        q_flux = q_coil / self.pipe.area_surf_outer

        # modified rayleigh number
        beta = self.water.beta(temperature)
        cond = self.water.conductivity(temperature)
        kin_visc = self.water.viscosity_kinematic(temperature)
        alpha = self.water.alpha(temperature)
        ra_star = gravity * abs(beta * q_flux) * (self.pipe.outer_dia ** 4) / (cond * kin_visc * alpha)

        # calculate convection coefficient
        if temperature > temperature_sw:
            a = 5.0
            b = 0.0317
            c = 0.333
            d = 0.344
            e = 0.301
        else:
            a = 5.75
            b = 0.00971
            c = 0.333
            d = 0.929
            e = 0.0

        nusselt = a + b * ra_star ** c * (self.dy / self.pipe.outer_dia) ** d * (self.dx / self.pipe.outer_dia) ** e
        h_o = nusselt * cond / self.pipe.outer_dia

        return 1 / (h_o * cond * self.pipe.area_surf_outer)

    def calc_inside_fouling_resistance(self, include_fouling=False):
        """
        Compute inside fouling resistance
        :param include_fouling: include fouling flag
        :return: inside fouling resistance, [K/W]
        """

        if include_fouling:
            return 0.000175 / self.pipe.area_surf_inner
        else:
            return 0.0

    def calc_outside_fouling_resistance(self, include_fouling=False):
        """
        Compute outside fouling resistance
        :param include_fouling: include fouling flag
        :return: outside fouling resistance, [K/W]
        """

        if include_fouling:
            return 0.00053 / self.pipe.area_surf_outer
        else:
            return 0.0

    def simulate(self, m_dot: Union[int, float],
                 inlet_temperature: Union[int, float],
                 water_temp: Union[int, float]):

        # initialize
        outlet_temperature = inlet_temperature
        outlet_temperature_iter = 0
        mean_temperature = inlet_temperature
        if inlet_temperature > water_temp:
            q_coil = 1000
        else:
            q_coil = -1000

        while abs(outlet_temperature - outlet_temperature_iter) > 0.01:
            outlet_temperature_iter = outlet_temperature

            r_inside_foul = self.calc_inside_fouling_resistance(self.include_inside_fouling)
            r_outside_foul = self.calc_outside_fouling_resistance(self.include_outside_fouling)
            r_inside_conv = self.calc_inside_conv_resistance(m_dot, mean_temperature)
            r_outside_conv = self.calc_outside_conv_resistance(q_coil, mean_temperature, water_temp)
            r_cond = self.pipe.calc_cond_resistance()
            r_total = r_inside_foul + r_outside_foul + r_inside_conv + r_outside_conv + r_cond

            ua = 1 / r_total

            cp_brine = self.brine.specific_heat(mean_temperature)
            ntu = ua / (m_dot * cp_brine)

            eff = 1 - exp(-ntu)

            q_max = m_dot * cp_brine * (inlet_temperature - water_temp)

            q_coil = eff * q_max

            mean_temperature = water_temp + m_dot * cp_brine * inlet_temperature * (
                    1 - exp(-ntu)) / ua + m_dot * cp_brine * water_temp * (-1 + exp(-ntu)) / ua

            outlet_temperature = inlet_temperature - q_coil / (m_dot * cp_brine)

        return outlet_temperature
