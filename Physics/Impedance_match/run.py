import numpy as np
import matplotlib.pyplot as plt

def ser(z1,z2):
    z=z1+z2
    return z

def par(z1,z2):
    z=1/(1/z1+1/z2)
    return z



fc=2e9

Z0=50

Zl=75
L=5.62e-9
C=1.5e-12
ZL=1j*2*np.pi*fc*L
ZC=1/(1j*2*np.pi*fc*C)
Gamma=(Zl-Z0)/(Zl+Z0)
print(f'Gamma={Gamma}')
print(f'abs(Gamma)={np.abs(Gamma)}')

print(f'ZL= {ZL} Ohm\nZC= {ZC} Ohm')
Ze=ser(ZL,par(ZC,Zl))
print(f'Ze={Ze} Ohm')
Gamma=(Ze-Z0)/(Ze+Z0)
print(f'Gamma={Gamma}')
print(f'abs(Gamma)={np.abs(Gamma)}')
print(f"""
  L= {L:.2e} H
--mm---------
       |    |
       =    0 Zl= {Zl} Ohm
       |    |
-------------
       C= {C:.2e} F
""")
