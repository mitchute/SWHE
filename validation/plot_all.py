import validation.plot_heat_pump_const_cop
import validation.plot_inside_conv_resistance
import validation.plot_outlet_temp_const_inlet_temp
import validation.plot_outlet_temp_const_mdot
import validation.plot_system

if __name__ == "__main__":
    validation.plot_heat_pump_const_cop.plot()
    validation.plot_inside_conv_resistance.plot()
    validation.plot_outlet_temp_const_inlet_temp.plot()
    validation.plot_outlet_temp_const_mdot.plot()
    validation.plot_system.plot()
