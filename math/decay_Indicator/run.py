import numpy as np
import matplotlib.pyplot as plt

def decay_Indicator0(v,val):
    sorted_v = np.sort(v)[::-1]
    print(sorted_v)
    print(v)
    for i in range(len(sorted_v)):
        if sorted_v[i] <= sorted_v[0]-val:
            return i
    return 0

def decay_Indicator(v,val):
    last_bigger_index=0
    for i in range(len(v)):
        # print(f"{v[i]>=v[0]}")
        if v[i] >= v[0]-val:
            last_bigger_index=i

    return last_bigger_index

val=10

for num in [96,343,485]:
    data=np.load(f"zeroDoppSlice_{num}.npy")
    plt.plot(data,".-")
    plt.axhline(data[0])
    plt.axhline(data[0]-val)
    plt.grid()
    plt.title(f"decay indicator: {decay_Indicator(data,val)}")
    plt.show()

# data96=np.load("zeroDoppSlice_96.npy")
# plt.plot(data96)
# plt.axhline(data96[0])
# plt.axhline(data96[0]-val)
# plt.grid()
# plt.title(f"decay indicator: {decay_Indicator(data96,val)}")
# plt.show()

# data343=np.load("zeroDoppSlice_343.npy")
# plt.plot(data343)
# plt.axhline(data343[0])
# plt.axhline(data343[0]-val)
# plt.grid()
# plt.title(f"decay indicator: {decay_Indicator(data343,val)}")
# plt.show()

# data485=np.load("zeroDoppSlice_485.npy")
# plt.plot(data485)
# plt.axhline(data485[0])
# plt.axhline(data485[0]-val)
# plt.grid()
# plt.title(f"decay indicator: {decay_Indicator(data485,val)}")
# plt.show()