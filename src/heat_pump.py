from typing import Union

from src.fluid import Fluid


class HeatPumpConstCOP(object):

    def __init__(self, data: dict):
        super().__init__()
        self.cop = data["cop"]
        self.fluid = Fluid(data["fluid"])

    def calc_cop(self):
        return self.cop

    def simulate_heating(self, q_zone: Union[int, float], m_dot_src: Union[int, float], inlet_temp: Union[int, float]):
        q_src = q_zone * (1 - 1 / self.cop)
        cp_f = self.fluid.specific_heat(inlet_temp)
        return inlet_temp - q_src / (m_dot_src * cp_f)

    def simulate_cooling(self, q_zone: Union[int, float], m_dot_src: Union[int, float], inlet_temp: Union[int, float]):
        q_src = q_zone * (1 + 1 / self.cop)
        cp_f = self.fluid.specific_heat(inlet_temp)
        return inlet_temp - q_src / (m_dot_src * cp_f)

    def simulate(self, q_zone: Union[int, float], m_dot_src: Union[int, float], inlet_temp_src: Union[int, float]):
        if q_zone > 0:
            return self.simulate_heating(q_zone, m_dot_src, inlet_temp_src)
        else:
            return self.simulate_cooling(q_zone, m_dot_src, inlet_temp_src)
