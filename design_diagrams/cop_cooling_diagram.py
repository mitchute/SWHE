import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize

from src.system import System

data = {
    "hp": {
        "cop": 3.0
    },
    "swhe": {
        "pipe": {
            "outer-dia": 0.02667,
            "inner-dia": 0.0215392,
            "length": 100,
            "density": 950,
            "conductivity": 0.4
        },
        "diameter": 1.2,
        "horizontal-spacing": 0.05,
        "vertical-spacing": 0.05,
    },
    "fluid": {
        "fluid-name": "PG",
        "concentration": 20
    }
}

system = System(data)


def obj_f(pipe_length, q_zone, m_dot, t_sw, t_appr_target):
    system.swhe.pipe.update_pipe(pipe_length)
    t_appr = system.simulate(q_zone, m_dot, t_sw)
    return (t_appr - t_appr_target) ** 2


def create_diagram():
    q_cooling = -3516.85
    t_appr = np.arange(1.5, 6.5, 0.25)

    pipe_length_init = 200
    pipe_length = [pipe_length_init]

    for t in t_appr:
        res = minimize(obj_f, x0=np.array([pipe_length[-1]]), args=(q_cooling, 0.5, 15, t))
        pipe_length.append(res.x[0])

    pipe_length.pop(0)
    pipe_length_norm_a = np.array(pipe_length) / abs(q_cooling) * 1000

    system.hp.cop = 4.0
    pipe_length = [pipe_length_init]

    for t in t_appr:
        res = minimize(obj_f, x0=np.array([pipe_length[-1]]), args=(q_cooling, 0.5, 15, t))
        pipe_length.append(res.x[0])

    pipe_length.pop(0)
    pipe_length_norm_b = np.array(pipe_length) / abs(q_cooling) * 1000

    system.hp.cop = 2.0
    pipe_length = [pipe_length_init]

    for t in t_appr:
        res = minimize(obj_f, x0=np.array([pipe_length[-1]]), args=(q_cooling, 0.5, 15, t))
        pipe_length.append(res.x[0])

    pipe_length.pop(0)
    pipe_length_norm_c = np.array(pipe_length) / abs(q_cooling) * 1000

    fig, ax = plt.subplots()
    ax.plot(t_appr, pipe_length_norm_a, label="COP = 3.0")
    ax.plot(t_appr, pipe_length_norm_b, label="COP = 4.0")
    ax.plot(t_appr, pipe_length_norm_c, label="COP = 2.0")
    ax.set_xlabel(r"Approach Temp [C]")
    ax.set_ylabel(r"m/kW")
    ax.legend()
    ax.grid()
    plt.show()


if __name__ == "__main__":
    create_diagram()
