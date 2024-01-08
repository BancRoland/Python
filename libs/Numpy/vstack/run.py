import numpy as np

a=np.floor((10*np.random.rand(10)))
b=np.floor((10*np.random.rand(10)))
c=np.vstack((a,b))
d=np.floor((10*np.random.rand(10)))
e=np.vstack((c,d))

print(a)
print(b)
print(c)
print(d)
print(e)