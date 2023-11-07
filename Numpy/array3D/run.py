import numpy as np
import matplotlib.pyplot as plt

arr3d=np.random.rand(5,6,3)

for i in range(np.shape(arr3d)[2]):
    plt.imshow(arr3d[:,:,i])
    plt.show()