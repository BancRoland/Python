import numpy as np

# https://www.itu.int/dms_pub/itu-r/opb/rep/R-REP-BO.2071-2-2019-PDF-E.pdf

R=36e6      # distance [m]
r=2000e3    # coverage radius [m]
P=14e3      # satellite power

print(P/(4*r**2*np.pi))
print("Sun intensity between 10-13 GHz -> 4.8e-11")