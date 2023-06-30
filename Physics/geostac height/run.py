import numpy as np
import matplotlib.pyplot as plt

alpha0=47.3
alpha=alpha0/180*np.pi
R=6371
d=42000

c=np.sqrt(R**2+d**2-2*R*d*np.cos(alpha))   #koszinusztétel
s=180-np.arcsin(np.sin(alpha)*d/c)/np.pi*180-90

print(f'Távolság az a adott szélességi körtől:\n {c:.2f} m')
print(f'Eleváció:\n {s:.2f} deg')