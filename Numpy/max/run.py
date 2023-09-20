import numpy as np
import matplotlib.pyplot as plt

n1=np.random.randn(100,100)
n2=np.random.randn(100,100)

plt.imshow(n1)
plt.show()

plt.imshow(n2)
plt.show()

plt.imshow(np.maximum(n1,n2))
plt.show()