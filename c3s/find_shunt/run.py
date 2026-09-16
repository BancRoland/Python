import matplotlib.pyplot as plt
import numpy as np


Resistors_available=np.array([
3780.168654
,2158.802027
,992.4478304
,556.7801136
,269.0652608
,149.6973225
,119.597736
,68.06416615
,38.75542692
,38.97691955
,19.45205479
,9.77131983
,4.888452435
])

power_on_resistors_while_measurement_watt = 1

max_voltage_on_PSU = 65
DAC_current_to_test_amper = 10

maximal_possible_power_on_largest_resisitor = max_voltage_on_PSU**2/max(Resistors_available)
print(f"{maximal_possible_power_on_largest_resisitor} V")


max_permitted_power_on_shunt_watt = 4

I=np.sqrt(power_on_resistors_while_measurement_watt/Resistors_available)


if 1:
    plt.title(f"Current on available resistor with measurement power:\n{power_on_resistors_while_measurement_watt} W")
    plt.xlabel("available resistor [Ohm]")
    plt.ylabel("current [A]")
    plt.plot(Resistors_available,I,"o-")
    plt.xscale("log")
    plt.yscale("log")


    plt.grid()
    plt.savefig("currents_on_resistors.png")
    plt.show()



check_maximal_shunt_vals_for_different_scenarios = True
if check_maximal_shunt_vals_for_different_scenarios:

    DAC_max_shunt_for_current = max_voltage_on_PSU/DAC_current_to_test_amper
    DAC_max_shunt_for_power = max_permitted_power_on_shunt_watt/DAC_current_to_test_amper**2
    print(DAC_max_shunt_for_current)

    maximal_permitted_shunt = max_permitted_power_on_shunt_watt/I**2
    maximal_shunt_to_keep_current_without_exceeding_power_limit = (max_voltage_on_PSU-Resistors_available*I)/I

    plt.figure(figsize=[10,7])

    plt.plot(Resistors_available,maximal_permitted_shunt,
             "o-", 
             color = "C0",
             label=f"while keeping work resistor power {power_on_resistors_while_measurement_watt} W,\nmax shunt to stay under shunt power: {max_permitted_power_on_shunt_watt} W\n neglecting PSU voltage")
    
    plt.plot(Resistors_available,maximal_shunt_to_keep_current_without_exceeding_power_limit,
             "o-", 
             color = "C1",
             label=f"max shunt to stay under PSU voltage: {max_voltage_on_PSU} V\nwhile keeping work resistor power: {power_on_resistors_while_measurement_watt} W\n neglecting shunt power")
    
    plt.axhline(DAC_max_shunt_for_power, 
                label=f"for DAC calibration not to exceed shunt power: {max_permitted_power_on_shunt_watt} W while testing current: {DAC_current_to_test_amper} A\nmaximal shunt: {DAC_max_shunt_for_power} Ohm",
                color="C0", 
                linestyle = "--")
    
    plt.axhline(DAC_max_shunt_for_current, 
                label=f"for DAC calibration to reach current: {DAC_current_to_test_amper} A, with PSU voltage: {max_voltage_on_PSU} V,\nmaximal shunt value: {DAC_max_shunt_for_current} Ohm",
                linestyle = "--",
                color="C1")

    plt.title(f"maximal permitted shunt value for each available resistor\nin order no to exceed shunt power: {max_permitted_power_on_shunt_watt} W\nwhile keeping work resistor power: {power_on_resistors_while_measurement_watt} W\n while not exceeding PSU voltage: {max_voltage_on_PSU} V\nminimum of these: {min(min(maximal_permitted_shunt),min(maximal_shunt_to_keep_current_without_exceeding_power_limit),DAC_max_shunt_for_current,DAC_max_shunt_for_power):.2f} Ohm")
    
    plt.xlabel("available resistor [Ohm]")
    plt.ylabel("resistor [Ohm]")
    
    plt.yscale("log")
    plt.xscale("log")

    plt.legend()
    # plt.axis("equal")
    plt.tight_layout()
    plt.xlim([1e0,1e4])
    plt.grid()
    plt.show()


example_shunt_val_ohm = 0.01

volages_on_psu_and_shunt = True
if volages_on_psu_and_shunt:
    voltage_on_shunt = example_shunt_val_ohm*I
    psu_voltage = I*(Resistors_available+example_shunt_val_ohm)
    plt.plot(Resistors_available,psu_voltage, "o-", label="Volage of PSU")
    plt.plot(Resistors_available,voltage_on_shunt, "o-", label="Volage on shunt")
             

    min_DAC_current_amp = 0.1
    max_DAC_shunt_volt = DAC_current_to_test_amper*example_shunt_val_ohm
    min_DAC_shunt_volt = min_DAC_current_amp*example_shunt_val_ohm
    plt.axhline(max_DAC_shunt_volt, label = f"maximal volt on shunt for DAC cal: {max_DAC_shunt_volt} V", color = "orange", linestyle = ":")
    plt.axhline(min_DAC_shunt_volt, label = f"minimal volt on shunt for DAC cal: {min_DAC_shunt_volt} V", color = "orange", linestyle = "--")
    plt.axhline(max_voltage_on_PSU, color = "red", label = f"max permitted voltage on PSU = {max(max(psu_voltage),max_voltage_on_PSU)} V")
    
    plt.yscale("log")
    plt.xscale("log")

    plt.grid()
    plt.legend()
    plt.ylabel(f"volatge [V]")
    plt.xlabel("available resistor [Ohm]")
    plt.show()

powers_on_shunt = True
if powers_on_shunt:
    power_on_shunt_for_res_meas = example_shunt_val_ohm*I**2
    plt.plot(Resistors_available, power_on_shunt_for_res_meas, "o-", label="power on shunt while resistor measurement")
             
    max_DAC_shunt_power = example_shunt_val_ohm * DAC_current_to_test_amper**2

    plt.axhline(max_DAC_shunt_power, label = f"maximal power on shunt for DAC cal: {max_DAC_shunt_power} W", color = "orange", linestyle = ":")

    plt.axhline(max_permitted_power_on_shunt_watt, color = "red", label = f"max permitted power on shunt = {max_permitted_power_on_shunt_watt} W")
    
    plt.yscale("log")
    plt.xscale("log")

    plt.grid()
    plt.legend()
    plt.ylabel(f"power [W]")
    plt.xlabel("available resistor [Ohm]")
    plt.show()











