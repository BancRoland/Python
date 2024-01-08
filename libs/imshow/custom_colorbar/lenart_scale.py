import matplotlib.pyplot as plt
import numpy as np

s=np.arange(0,1024)/1024
r=s
g=(2*s)%1
b=(4*s)%1
colors_Lenart=np.zeros([1024,3])

for i in range(1024):
    colors_Lenart[i,0]=r[i]
    colors_Lenart[i,1]=g[i]
    colors_Lenart[i,2]=b[i]

plt.plot(s, r, 'o-', color='red')
plt.plot(s, g, 'o-', color='green')
plt.plot(s, b, 'o-', color='blue')
plt.show()


print(colors_Lenart)