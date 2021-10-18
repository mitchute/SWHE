from src.pipe import Pipe


class SWHE(object):
    def __init__(self, data):
        # pipe data
        self.pipe = Pipe(data["pipe"])

    def calc_fluid_velocity(self, m_dot):
        """
        Calculate mean fluid velocity inside pipe
        :param m_dot: mass flow rate, kg/s
        :return: mean fluid velocity, m/s
        """
        return 42

    def calc_inside_conv_resistance(self, m_dot):
        """
        Compute inside convection resistance
        :param m_dot: mass flow rate, kg/s
        :return: resistance, K/W
        """
        return 42
