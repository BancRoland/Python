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

# Resistors_target0=[
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

# plt.plot(Resistors_target)
# plt.show()

Resistors_target = np.array(Resistors_target)


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
for i in range(len(Resistors_target)):
    print(f"#{i}:\t{Resistors_target[i]}")

print("\n")

matches = closest_combinations(Resistors_available, Resistors_target)

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
# plt.scatter(Resistors_target, Resistors_target, color='gray', label='Available resistors', marker='o', alpha=0.5)

# Plot target values as red Xs
plt.scatter(Resistors_target, Resistors_target, color='C0', label='Target values', marker='+', s=200, zorder=0)

# Plot step function connecting target indices to their best match
plt.step(Resistors_target, best_values, where='mid', color='grey', linestyle="--", linewidth=1, zorder=1, alpha=0.7)

# Also plot best matches as green triangles for clarity
plt.scatter(Resistors_target, best_values, color='C1', marker='.', s=40, zorder=2, label='Best matches')

# # Annotate with indexes
# for i, m in enumerate(matches):
#     idxs = [Resistors_available.index(r) for r in m["combination"]]
#     plt.text(Resistors_target[i], best_values[i], f"{idxs}", fontsize=8, ha='left', va='bottom')

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
# plt.scatter(Resistors_target, Resistors_target, color='gray', label='Available resistors', marker='o', alpha=0.5)

diff= np.abs(best_values-Resistors_target)

# Also plot best matches as green triangles for clarity
plt.scatter(Resistors_target, diff, color='C1', marker='.', s=40, zorder=2, label='Best matches')

# Plot step function connecting target indices to their best match
plt.step(Resistors_target, diff, where='mid', color='grey', linewidth=1, zorder=1, alpha=0.7, linestyle="--")

# # Annotate with indexes
# for i, m in enumerate(matches):
#     idxs = [Resistors_available.index(r) for r in m["combination"]]
#     plt.text(Resistors_target[i], best_values[i], f"{idxs}", fontsize=8, ha='left', va='bottom')

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
# plt.scatter(Resistors_target, Resistors_target, color='gray', label='Available resistors', marker='o', alpha=0.5)

diff_percent= np.abs((best_values-Resistors_target)/Resistors_target*100)

# Also plot best matches as green triangles for clarity
plt.scatter(Resistors_target, diff_percent, color='C1', marker='.', s=40, zorder=2, label='Best matches')

# Plot step function connecting target indices to their best match
plt.step(Resistors_target, diff_percent, where='mid', color='grey', linestyle="--", linewidth=1, zorder=1, alpha=0.7)


# # Annotate with indexes
# for i, m in enumerate(matches):
#     idxs = [Resistors_available.index(r) for r in m["combination"]]
#     plt.text(Resistors_target[i], best_values[i], f"{idxs}", fontsize=8, ha='left', va='bottom')

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
