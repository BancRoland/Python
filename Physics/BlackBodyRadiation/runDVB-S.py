import numpy as np
import matplotlib.pyplot as plt
from os import system
system("cat header.txt")

T=5778
k_B=1.380649E-23 #[J/K] Boltzmann állandó
R_S=696_340_000 #[m] földtávolság
R_T=150E9 #[m] földtávolság

f_min=10e9
f_max=13e9
RES=100

# # látható tartományra számítva
# f_min=400E12
# f_max=790E12

# # kvázi teljes tartományra számítva
# f_min=100e6
# f_max=2E15

# f_step=1e6
f_step=(f_max-f_min)/RES
f=np.arange(f_min,f_max,f_step)

c=3E8 #[m/s] speed of light
h=6.62607015E-34 #[J/Hz]
sigma=5.67E-8   #[W/m^2/K^4]

T=5778  #[K]
lmbda=c/f


B=2*h*(f**3)/(c**2*(np.exp(h*f/k_B/T)-1))
plt.plot(f,B,'.-')
plt.grid()
plt.title(f'Nap felsznére számított sugárintenzitás')
plt.xlabel("frekvencia [Hz]")
plt.ylabel("Intenzitás [W/m^2/srad]")
plt.show()

A_S=4*R_S**2*np.pi
A_T=4*R_T**2*np.pi
P_plnk=np.sum(B*f_step)*A_S*np.pi #itt nem kell 4-es szorzó, mert Lambert felület
P_stp=A_S*sigma*T**4
print(f'Vizsgált frekvenciasáv:\n\033[1m{f_min:.2e} Hz - {f_max:.2e} Hz\033[0m')
print(f'output according to Plank\t\033[1m{P_plnk:.2e} W\033[0m')
print(f'output according to Stephan\t\033[1m{P_stp:.2e} W\033[0m')
S=P_plnk/A_T
print(f'Adott sávra vett Napállandó:\t\033[1m{S:.2e} W/m^2\033[0m')
print(f'Adott sávra vett Napállandó:\t\033[1m{10*np.log10(S*1000):.2f} dBm\033[0m')

Z=B*A_S*np.pi/A_T
plt.plot(f,Z,'.-')
plt.grid()
plt.title(f'Napból felületegységre érkező teljesítményeloszlás\nAdott tartományra számított Napállandó= \n{S:.2e} W/m^2')
plt.xlabel("frekvencia [Hz]")
plt.ylabel("Intenzitás [W/m^2/Hz]")
plt.show()
