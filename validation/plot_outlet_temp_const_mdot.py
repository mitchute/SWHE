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

    x = np.arange(1, 40, 0.1)
    y_010 = [swhe.simulate(0.10, m, 20) for m in x]
    y_050 = [swhe.simulate(0.50, m, 20) for m in x]
    y_100 = [swhe.simulate(1.00, m, 20) for m in x]

    fig, ax = plt.subplots()
    ax.plot(x, x, label=r"$T_{in}$")
    ax.plot(x, y_010, label=r"$T_{out}$ $\dot{m}=0.10$ kg/s")
    ax.plot(x, y_050, label=r"$T_{out}$ $\dot{m}=0.50$ kg/s", linestyle="--")
    ax.plot(x, y_100, label=r"$T_{out}$ $\dot{m}=1.00$ kg/s", linestyle=":")
    ax.plot([1, 40], [20, 20], label=r"$T_{sw}$")
    ax.set_xlabel(r"$T$ [C]")
    ax.set_ylabel(r"$T$ [C]")
    ax.legend()
    ax.grid()
    f_name = Path(__file__).parent / "outlet_temp_const_mdot.png"
    plt.savefig(f_name, bbox_inches="tight")


if __name__ == "__main__":
    plot()
