import numpy as np
import matplotlib.pyplot as plt

LEN=100
NUM=10
arr=np.zeros([LEN,NUM])
for i in range(NUM):
    vec=np.random.randn(LEN)
    arr[:,i]=vec
print(vec)