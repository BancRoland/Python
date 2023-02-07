import numpy as np
import matplotlib.pyplot as plt

f=open('dat.txt')
lines= f.read()
lines=lines.replace("\n", "")
lines=lines.replace("\t", "")
lines=lines.replace(" ", "")
nums0=lines.split(",")
nums=np.zeros(len(nums0))
for i in range(len(nums)):
    # print(eval(nums0[i]))
    nums[i]=eval(nums0[i])

print(nums)
plt.plot(nums,'.-')
plt.show()