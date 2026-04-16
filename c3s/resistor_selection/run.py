import matplotlib.pyplot as plt
import numpy as np
from resistors_target import Resistors_target
import itertools

def parallel(*resistors):
    """Return equivalent resistance of resistors in parallel."""
    return 1 / sum(1/r for r in resistors)

def all_parallel_combinations(resistors):
    results = []
    n = len(resistors)
    for k in range(1, n + 1):
        for combo in itertools.combinations(resistors, k):
            req = parallel(*combo)
            results.append((combo, req))  # store tuple: (combo, equivalent resistance)
    return results

def closest_combinations(available, targets):
    """For each target resistance, find the closest parallel combo."""
    combos = all_parallel_combinations(available)
    results = []
    for target in targets:
        best = min(combos, key=lambda x: abs(x[1] - target))
        results.append({
            "target": target,
            "closest_value": best[1],
            "difference": abs(best[1] - target),
            "combination": best[0]
        })
    return results



Resistors_available=[
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
]

Resistors_available_binary=[
4096
,2048
,1024
,512
,256
,128
,64
,32
,16
,8
,4
]

# possible_resistor_combinations0=[
# 3900
# ,2200
# ,1000
# ,560
# ,270
# ,150
# ,120
# ,68
# ,39
# ,39
# ,19.5
# ,9.75
# ,4.875
# ]

# plt.plot(possible_resistor_combinations)
# plt.show()

TEST_FOR_BINARY=0

if TEST_FOR_BINARY:
    possible_resistor_combinations0 = all_parallel_combinations(Resistors_available_binary)
    equivalent_resistances = [combo_req[1] for combo_req in possible_resistor_combinations0]
    equivalent_resistances=np.sort(equivalent_resistances)[::-1]
    possible_resistor_combinations=equivalent_resistances
else:
    possible_resistor_combinations = Resistors_target   


plt.figure(figsize=[8,6])
plt.plot(possible_resistor_combinations,".-")
plt.grid()
plt.title("Possible resistor values")
plt.xlabel("resistor index []")
plt.ylabel("resistance [Ohm]")
plt.savefig(f"possible_resistors.png")
# plt.show()
plt.close()


used_voltage = 52 # [V]
currents_of_adjacent_resistors =[]

def get_plots(possible_resistor_combinations, used_voltage,marker,current_limit):
    possible_resistor_combinations = np.array(possible_resistor_combinations)
    currents_of_adjacent_resistors=used_voltage/possible_resistor_combinations
    plt.figure(figsize=[8,6])
    plt.plot(currents_of_adjacent_resistors,".-")
    plt.plot([0,len(possible_resistor_combinations)],[0,len(possible_resistor_combinations)*current_limit],":",alpha=1,color="gray")
    plt.grid()
    plt.ylabel("current [A]")
    plt.xlabel("resistor index []")
    plt.title(f"Possible currents with adjacent resistance steps\nat current limit: {current_limit*1000} mA\nnumber of resistor options = {len(currents_of_adjacent_resistors)}")
    plt.tight_layout()
    plt.savefig(f"available_current_vals_{current_limit*1000}.png")
    # plt.show()
    plt.close()

    diff_current = currents_of_adjacent_resistors[1:]-currents_of_adjacent_resistors[0:-1]
    plt.figure(figsize=[8,6])
    plt.plot(diff_current)
    plt.plot(diff_current,"o")
    plt.axhline(current_limit,color="red",alpha=1,linestyle=":")
    plt.grid()
    plt.ylabel("current differnece [A]")
    plt.xlabel("resistor index []")
    plt.ylim(bottom=0)
    plt.title(f"Current difference between adjacent resistance steps\nat current limit: {current_limit*1000} mA\nnumber of resistor options = {len(currents_of_adjacent_resistors)}")
    plt.tight_layout()
    plt.savefig(f"finest_current_steps_{current_limit*1000}.png")
    # plt.show()
    plt.close()
    
    return currents_of_adjacent_resistors, diff_current
    

# current_limit_list = [0,5e-3,10e-3,15e-3,20e-3,25e-3,30e-3,35e-3,40e-3,50e-3,60e-3,75e-3,100e-3]
current_limit_list = [50e-3]

basepass_current_limit = 10e-3
    
for current_limit in current_limit_list:
    
# currents_of_adjacent_resistors,diff_current=get_plots(possible_resistor_combinations, used_voltage, "basic", current_limit = current_limit)

    calculate_steps_method = 1
    if calculate_steps_method:
        ultimate_resistors = [possible_resistor_combinations[0]]
        for i in range(len(possible_resistor_combinations)-1):
            current_before = used_voltage/ultimate_resistors[-1]
            current_now = used_voltage/possible_resistor_combinations[i]
            current_future = used_voltage/possible_resistor_combinations[i+1]
            
            diff_before = (current_now - current_before)
            diff_future = (current_future - current_before)
            
            # print(f"current_before = {current_before}")
            # print(f"current_now = {current_now}")
            # print(f"current_future = {current_future}")
            # print(f"diff_before = {diff_before} -> {(diff_before <= current_limit)}")
            # print(f"diff_future = {diff_future} -> {(diff_future >current_limit)}")
            # print()
            # import time
            # time.sleep(2)
            
            under_basepass_limit = (diff_before <= basepass_current_limit) and  (diff_future >basepass_current_limit)
            if under_basepass_limit:
                print("WOW")
            
            found_border = (diff_before <= current_limit) and  (diff_future >current_limit)
            if found_border:
                print("HURRAY")
                
            alreaady_over = (diff_before > current_limit) and  (diff_future >current_limit)
            if alreaady_over:
                print("OH NO!")
            
            if (found_border or alreaady_over or under_basepass_limit) and (possible_resistor_combinations[i] != ultimate_resistors[-1]) :
                ultimate_resistors.append(possible_resistor_combinations[i])
                
                
                
            
        print(len(possible_resistor_combinations)) 
        print(len(ultimate_resistors))
                
        get_plots(ultimate_resistors, used_voltage,f"calStep_{current_limit}",current_limit=current_limit)        
        
        
        
        
        
        
        
        
    find_clossest_resistor_method=0
    if find_clossest_resistor_method:
        def get_closest_resistor_for_target_current(target_current):
            for i in range(len(currents_of_adjacent_resistors)-1):
                if (currents_of_adjacent_resistors[i]<=target_current) and (currents_of_adjacent_resistors[i+1]>target_current):
                    print(target_current)
                    print(currents_of_adjacent_resistors[i])
                    print()
                    return possible_resistor_combinations[i]
            return -1

        ultimate_resistors = []

        get_resistor_for_current=1
        min_current=min(currents_of_adjacent_resistors)
        max_current=max(currents_of_adjacent_resistors)

        current_checkpoints = np.arange(min_current,max_current,current_limit)

        for current in current_checkpoints:
            ultimate_resistors.append(get_closest_resistor_for_target_current(current))
            
        plt.plot(ultimate_resistors)
        plt.show()
            
        print(len(ultimate_resistors))
        get_plots(ultimate_resistors,used_voltage,2)
            

raise
def make_tipmix_chart(ON_indexes,all_num):
    v=np.zeros(all_num)
    for i in range(len(ON_indexes)):
        v[ON_indexes]=1
    print(v)
    for i in v:
        if i:
            print("#", end="")
        else:
            print("O", end="")
    print("")

print(f"I have these resistors:")
for i in range(len(Resistors_available)):
    print(f"#{i}:\t{Resistors_available[i]}")

print("\n")
print(f"I want these resistors:")
for i in range(len(possible_resistor_combinations)):
    print(f"#{i}:\t{possible_resistor_combinations[i]}")

print("\n")

matches = closest_combinations(Resistors_available, possible_resistor_combinations)

for m in matches:
    diff_percent=m['difference']/m["target"]*100
    indexes = [Resistors_available.index(r) for r in m["combination"]]

    print(f"Target: {m['target']} Ω")
    # print(f"Closest: {m['closest_value']:.2f} Ω using {m['combination']}")
    print(f"Closest: {m['closest_value']:.6f} Ω using indexes {indexes}\n(values {m['combination']})")
    make_tipmix_chart(indexes,len(Resistors_available))
    print(f"Difference: {m['difference']:.6f} Ω\t{diff_percent:.1f} %\n")








# Extract best matches
best_values = np.array([m["closest_value"] for m in matches])

# Create a figure
plt.figure(figsize=(10, 6))

# # Plot available resistor values as gray dots (optional for reference)
# plt.scatter(possible_resistor_combinations, possible_resistor_combinations, color='gray', label='Available resistors', marker='o', alpha=0.5)

# Plot target values as red Xs
plt.scatter(possible_resistor_combinations, possible_resistor_combinations, color='C0', label='Target values', marker='+', s=200, zorder=0)

# Plot step function connecting target indices to their best match
plt.step(possible_resistor_combinations, best_values, where='mid', color='grey', linestyle="--", linewidth=1, zorder=1, alpha=0.7)

# Also plot best matches as green triangles for clarity
plt.scatter(possible_resistor_combinations, best_values, color='C1', marker='.', s=40, zorder=2, label='Best matches')

# # Annotate with indexes
# for i, m in enumerate(matches):
#     idxs = [Resistors_available.index(r) for r in m["combination"]]
#     plt.text(possible_resistor_combinations[i], best_values[i], f"{idxs}", fontsize=8, ha='left', va='bottom')

# Labels and formatting
plt.title("Approximation of target resistances with parellel combination of available ones")
plt.xlabel("Target resistance [Ω]")
plt.ylabel("Resistance [Ω]")
plt.legend()

# Major grid
plt.grid(which='major', linestyle='-', linewidth=0.75)
# Minor grid
plt.grid(which='minor', linestyle=':', linewidth=0.25, color='gray')

plt.tight_layout()

plt.xscale('log')
plt.yscale('log')

plt.savefig("approx.png")

plt.show()





# Create a figure
plt.figure(figsize=(10, 6))

# # Plot available resistor values as gray dots (optional for reference)
# plt.scatter(possible_resistor_combinations, possible_resistor_combinations, color='gray', label='Available resistors', marker='o', alpha=0.5)

diff= np.abs(best_values-possible_resistor_combinations)

# Also plot best matches as green triangles for clarity
plt.scatter(possible_resistor_combinations, diff, color='C1', marker='.', s=40, zorder=2, label='Best matches')

# Plot step function connecting target indices to their best match
plt.step(possible_resistor_combinations, diff, where='mid', color='grey', linewidth=1, zorder=1, alpha=0.7, linestyle="--")

# # Annotate with indexes
# for i, m in enumerate(matches):
#     idxs = [Resistors_available.index(r) for r in m["combination"]]
#     plt.text(possible_resistor_combinations[i], best_values[i], f"{idxs}", fontsize=8, ha='left', va='bottom')

# Labels and formatting
plt.title("Absolute Difference between nominal and measured resistor values for the optimal match")
plt.xlabel("Target resistance [Ω]")
plt.ylabel("Absolute resistance difference [Ω]")
plt.legend()

# Major grid
plt.grid(which='major', linestyle='-', linewidth=0.75)
# Minor grid
plt.grid(which='minor', linestyle=':', linewidth=0.5, color='gray')

plt.tight_layout()

plt.xscale('log')
plt.yscale('log')

plt.savefig("abs_diff.png")


plt.show()






# Create a figure
plt.figure(figsize=(10, 6))

# # Plot available resistor values as gray dots (optional for reference)
# plt.scatter(possible_resistor_combinations, possible_resistor_combinations, color='gray', label='Available resistors', marker='o', alpha=0.5)

diff_percent= np.abs((best_values-possible_resistor_combinations)/possible_resistor_combinations*100)

# Also plot best matches as green triangles for clarity
plt.scatter(possible_resistor_combinations, diff_percent, color='C1', marker='.', s=40, zorder=2, label='Best matches')

# Plot step function connecting target indices to their best match
plt.step(possible_resistor_combinations, diff_percent, where='mid', color='grey', linestyle="--", linewidth=1, zorder=1, alpha=0.7)


# # Annotate with indexes
# for i, m in enumerate(matches):
#     idxs = [Resistors_available.index(r) for r in m["combination"]]
#     plt.text(possible_resistor_combinations[i], best_values[i], f"{idxs}", fontsize=8, ha='left', va='bottom')

# Labels and formatting
plt.title("Relative difference between nominal and measured resistor values for the optimal match")
plt.xlabel("Target Resistance [Ω]")
plt.ylabel("relative difference [%]")
plt.legend()

# Major grid
plt.grid(which='major', linestyle='-', linewidth=0.75)
# Minor grid
plt.grid(which='minor', linestyle=':', linewidth=0.5, color='gray')

plt.tight_layout()

plt.axhline(1,linestyle="--",linewidth=1, color="black")
plt.axhline(5,linestyle="--",linewidth=1, color="black")
plt.text(2,1.1," 1% threshold line", color="black")
plt.text(2,5.5," 5% threshold line", color="black")


plt.xscale('log')
plt.yscale('log')

plt.savefig("abs_rel_diff.png")


plt.show()
