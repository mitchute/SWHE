from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from src.swhe import SWHE


def plot():
    data = {
        "pipe": {
            "outer-dia": 0.02667,
            "inner-dia": 0.0215392,
            "length": 100,
            "density": 950,
            "conductivity": 0.4
        },
        "fluid": {
            "fluid-name": "PG",
            "concentration": 20
        },
        "diameter": 1.2,
        "horizontal-spacing": 0.05,
        "vertical-spacing": 0.05,
    }
    swhe = SWHE(data)

    x = np.arange(0.01, 1, 0.01)
    y = [swhe.simulate(m, 25, 20) for m in x]

    fig, ax = plt.subplots()
    ax.plot([0, 1], [25, 25], label=r"$T_{in}$")
    ax.plot(x, y, label=r"$T_{out}$")
    ax.plot([0, 1], [20, 20], label=r"$T_{sw}$")
    ax.set_xlabel(r"$\dot{m}$ [kg/s]")
    ax.set_ylabel(r"$T$ [C]")
    ax.legend()
    ax.grid()
    f_name = Path(__file__).parent / "outlet_temp_const_inlet_temp.png"
    plt.savefig(f_name, bbox_inches="tight")


if __name__ == "__main__":
    plot()
