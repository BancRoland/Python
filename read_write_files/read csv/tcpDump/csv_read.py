import matplotlib.pyplot as plt
import csv
import numpy as np
from datetime import datetime
import math

time_samples = []  # Array to store the time samples
data_sizes = []

# Open the file
with open("dumpTX.log", "r") as file:
    # Read each line in the file
    for line in file:
        split_line = line.split()
        
        # Extract the first element (time sample)
        time_sample_str = split_line[0]
        data_size = split_line[7]

        # Convert the time sample string to datetime format
        time_sample = datetime.strptime(time_sample_str, "%H:%M:%S.%f")
        
        # Add the time sample to the array
        time_samples.append(time_sample)
        data_sizes.append(float(data_size))

# Print the time samples
x = range(len(time_samples))

# # Plot the time samples
# plt.plot(x, time_samples, '.-')
# plt.xlabel("Sample Index")
# plt.ylabel("Time")
# plt.title("Time Samples")
# plt.show()


plt.plot(data_sizes, '.')
plt.xlabel("Sample Index")
plt.ylabel("Time")
plt.title("Time Samples")
plt.show()



diff=[]

for i in range(len(x)-1):
    diff0=float((time_samples[i+1]-time_samples[i]).total_seconds())
    diff.append(diff0)
    # print(diff0)
diff.append(0.01)

# print(diff)
    

# Plot the time samples
plt.plot(np.log10(diff), '.-')
plt.xlabel("Sample Index")
plt.ylabel("Time difference")
plt.title("Time differneces between samples")
plt.show()

# speed=np.array(data_sizes)/np.array(diff)
Data=np.array(data_sizes)
Diff=np.array(diff)
print(Data)
print(Diff)
# print(len(data_sizes))
# print(len(diff))
plt.plot(Data/Diff,'o')
plt.show()