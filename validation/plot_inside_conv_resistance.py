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

    x = np.arange(0.01, 0.5, 0.001)
    y = [swhe.calc_inside_conv_resistance(m, 20) for m in x]

    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_yscale("log")
    ax.set_xlabel(r"$\dot{m}$ [kg/s]")
    ax.set_ylabel(r"$R_{conv}$ [K/W]")
    ax.grid()
    plt.title("Inside Convection Resistance")
    f_name = Path(__file__).parent / "_inside_conv_resistance.png"
    plt.savefig(f_name, bbox_inches="tight")


if __name__ == "__main__":
    plot()
