import peakutils
import numpy as np
import matplotlib.pyplot as plt

def findSLL(data):
    center=int(len(data)/2)

    peak_indices = peakutils.indexes(data)
    peak_heights = data[peak_indices]
    sorted_peaks_idx = np.argsort(peak_heights)[::-1]
    
    sorted_data_idx = np.argsort(data)[::-1]
    if center==sorted_data_idx[0]:
        SLL=data[center]-data[peak_indices[sorted_peaks_idx[1]]]
    else:
        SLL=data[center]-data[peak_indices[sorted_peaks_idx[0]]]
    return SLL

# data = np.array([0, 1, 3, 2, 1, 4, 2, 0])
data = np.load('data.npy')

th=0.75

# peak_indices = peakutils.indexes(data, thres=th, min_dist=10)
print("Peaks")
peak_indices = peakutils.indexes(data)
peak_heights = data[peak_indices]
print(peak_indices)
print(peak_heights)

print("Sorted peaks")
sorted_peaks_idx = np.argsort(peak_heights)[::-1]
sorted_peaks_val = np.argsort(peak_heights)[::-1]
print(sorted_peaks_idx)
print(sorted_peaks_val)


# Get the indices that would sort the array
sorted_indices = np.argsort(data)[::-1]
print(sorted_indices)
print(data)
print(data[sorted_indices[0]])
print(data[sorted_indices[1]])
print(int(len(data)/2))

# Sort the array and original indices
sorted_array = data[sorted_indices]


center=int(len(data)/2)
# sorted_val =data.sort(reverse=True)
# second_max = sorted_val[1]
SLL=data[center]-data[sorted_indices[1]]


plt.plot(data)
plt.scatter(peak_indices, peak_heights, c="black", marker='.')
plt.axvline(center,linestyle=":",alpha=0.8,color="black")
plt.scatter(sorted_indices[0],data[sorted_indices[0]], c="blue", marker="o")
plt.scatter(peak_indices[sorted_peaks_idx[1]],data[peak_indices[sorted_peaks_idx[1]]], c="red", marker="o")
plt.axhline(th*(np.max(data)-np.min(data))+np.min(data),linestyle="--",alpha=1,color="black")
plt.axhline(np.min(data),linestyle=":",alpha=0.8,color="black")
plt.axhline(np.max(data),linestyle=":",alpha=0.8,color="black")
plt.axhline(max(data)-findSLL(data),linestyle='--',color="yellow")
plt.title(f"SLL = {SLL:.2f} dB\nSLL = {findSLL(data):.2f} dB")
plt.xlabel('Data Index')
plt.ylabel('Data Value')
plt.grid()
plt.show()