from typing import Union

from src.heat_pump import HeatPumpConstCOP
from src.swhe import SWHE


class System(object):
    def __init__(self, data: dict):
        self.hp = HeatPumpConstCOP({**data["hp"], "fluid": data["fluid"]})
        self.swhe = SWHE({**data["swhe"], "fluid": data["fluid"]})

    def simulate(self, q_zone: Union[int, float], m_dot: Union[int, float], temperature_sw: Union[int, float]):
        """
        Simulate system containing a heat pump and surface water heat exchanger
        :param q_zone: zone load, [W]
        :param m_dot: mass flow rate through swhe, [kg/s]
        :param temperature_sw:
        :return:
        """

        t_appr = 0
        t_appr_old = 5
        t_out_swhe = temperature_sw
        tol = 0.01

        while abs(t_appr - t_appr_old) > tol:
            t_appr_old = t_appr
            t_out_hp = self.hp.simulate(q_zone, m_dot, t_out_swhe)
            t_out_swhe = self.swhe.simulate(m_dot, t_out_hp, temperature_sw)
            t_appr = t_out_swhe - temperature_sw

        return t_appr
