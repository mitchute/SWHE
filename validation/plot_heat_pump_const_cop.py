from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from src.heat_pump import HeatPumpConstCOP


def plot():
    d = {
        "cop": 3.0,
        "fluid": {
            "fluid-name": "PG",
            "concentration": 20
        },
    }

    hp = HeatPumpConstCOP(d)

    x = np.arange(-3000, 3000, 100)
    y_a = [hp.simulate(m, 0.1, 15) for m in x]
    y_b = [hp.simulate(m, 0.25, 15) for m in x]
    y_c = [hp.simulate(m, 1.0, 15) for m in x]
    fig, ax = plt.subplots()
    ax.plot([-3000, 3000], [15, 15], label=r"$T_{in,src}$")
    ax.plot(x, y_a, label=r"$T_{out,src}$ $\dot{m}=0.10$ [kg/s]")
    ax.plot(x, y_b, label=r"$T_{out,src}$ $\dot{m}=0.25$ [kg/s]", linestyle="--")
    ax.plot(x, y_c, label=r"$T_{out,src}$ $\dot{m}=1.00$ [kg/s]", linestyle=":")

    ax.set_xlabel(r"$\dot{q}_{zone}$ [W]")
    ax.set_ylabel(r"$T_{out,src}$ [C]")
    ax.legend()
    ax.grid()
    f_name = Path(__file__).parent / "heat_pump_const_cop.png"
    plt.savefig(f_name, bbox_inches="tight")


if __name__ == "__main__":
    plot()
