from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from src.system import System


def plot():
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

    x = np.arange(-3000, 3000, 200)
    y_a = [system.simulate(m, 0.1, 15) for m in x]
    y_b = [system.simulate(m, 0.25, 15) for m in x]
    y_c = [system.simulate(m, 1.0, 15) for m in x]
    fig, ax = plt.subplots()
    ax.plot(x, y_a, label=r"$T_{appr}$ $\dot{m}=0.10$ [kg/s]")
    ax.plot(x, y_b, label=r"$T_{appr}$ $\dot{m}=0.25$ [kg/s]", linestyle="--")
    ax.plot(x, y_c, label=r"$T_{appr}$ $\dot{m}=1.00$ [kg/s]", linestyle=":")

    ax.set_xlabel(r"$\dot{q}_{zone}$ [W]")
    ax.set_ylabel(r"$T_{appr}$ [C]")
    ax.legend()
    ax.grid()
    f_name = Path(__file__).parent / "_system_approach_temp.png"
    plt.savefig(f_name, bbox_inches="tight")


if __name__ == "__main__":
    plot()
