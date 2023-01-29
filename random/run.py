import numpy as np
import matplotlib.pyplot as plt

my_dpi=96

size=100
r=np.random.rand(size, size)
plt.figure(figsize=(size/my_dpi, size/my_dpi), dpi=my_dpi)
plt.imshow(r)
plt.savefig("fig.png")
plt.show()
