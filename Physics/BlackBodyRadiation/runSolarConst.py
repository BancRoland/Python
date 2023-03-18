import numpy as np
import matplotlib.pyplot as plt
from os import system
system("cat header.txt")

T=5778 #[K] Sun surface temperature
k_B=1.380649E-23 #[J/K] Boltzmann constant
R_S=696_340_000 #[m] Sun radius
R_T=150E9 #[m] Astonomical unit
# f=10E12  #[Hz]    vizsgált frekvencia
f=np.arange(6e13,2e15,1e13) #[Hz] frequency range
f_RED=400e12 #[Hz] 
f_BLUE=790e12 #[Hz]
c=3E8 #[m/s] speed of light
h=6.62607015E-34 #[J/Hz] Planck constant
sigma=5.67E-8   #[W/m^2/K^4] Stefan–Boltzmann law 

T0=np.arange(1000,7000,1000) #[K]
T02=np.append(T0,T)
T0str = [str(x)+" K" for x in T02]
lmbda=c/f #[m]

f_e12=f/1e12
plt.plot()
for i in range(len(T0)):
    B=2*h*f**3 /( c**2*(np.exp(h*f/k_B/T0[i])-1) ) #[J*sec*m^2/sec^2/m^5] = [J/sec/m^3]
    plt.plot(f_e12,B,'.-', color=(0.8*i/(len(T0)-1),0.8*i/(len(T0)-1),0.8*i/(len(T0)-1)))
B=2*h*(f**3)/((c**2)*np.exp(h*f/k_B/T)-1) #[J*sec*m^2/sec^2/m^5] = [J/sec/m^3]
plt.plot(f_e12,B,'--', color=(0,0,0))
plt.grid()
plt.legend(T0str)
plt.axvline(x=f_RED/1e12, color='r', linestyle='-')
plt.axvline(x=f_BLUE/1e12, color='b', linestyle='-')
plt.text(f_RED/1e12, 4e-8, 'Visible Spectrum', fontsize = 10)
plt.xlabel("frekvencia [THz]")
plt.ylabel("Intenzitás [W/m^2/srad]")
plt.title("Feketetest sugárzás")
plt.show()

lmbda_e9=lmbda*1e9
plt.plot()
for i in range(len(T0)):
    B=2*h*c**2 /(lmbda**5 *(np.exp(h*c/lmbda/k_B/T0[i])-1) ) #[J*sec*m^2/sec^2/m^5] = [J/sec/m^3]
    plt.plot(lmbda_e9,B,'.-', color=(0.8*i/(len(T0)-1),0.8*i/(len(T0)-1),0.8*i/(len(T0)-1)))

B=2*h*c**2 /(lmbda**5 *(np.exp(h*c/lmbda/k_B/T)-1) )
plt.plot(lmbda_e9,B,'--', color=(0,0,0))
plt.title("Planck sugárzási törvénye")
plt.grid()
plt.legend(T0str)
plt.axvline(x=c/f_RED*1e9, color='r', linestyle='-')
plt.axvline(x=c/f_BLUE*1e9, color='b', linestyle='-')
plt.text(c/f_BLUE*1e9, 3e13, 'Visible Spectrum', fontsize = 10)
plt.xlabel("hullámhossz [nm]")
plt.ylabel("Intenzitás [W/m^2/srad]")
plt.title("Feketetest sugárzás")
plt.show()

# !!!A frekveniában mérhető maximum nem felel meg a hullámhosszban mérhető maximummal!!!
# plt.plot()
# for T in T0:
#     B=2*h*f**5 /( c**3*(np.exp(h*f/k_B/T)-1) )
#     # B=2*h*(f**3)/((c**2)*np.exp(h*f/k_B/T)-1)
#     # B=(f**3)
#     # B=2*h*c**2 /(lmbda**5 *(np.exp(h*c/lmbda/k_B/T)-1) )
#     # plt.plot(f/1e12,B,'.-')
#     plt.plot(f,B,'.-')
# T=5778 #[K]
# B=2*h*f**5 /( c**3*(np.exp(h*f/k_B/T)-1) )
# plt.plot(f,B,'--')
# plt.grid()
# plt.legend(T0)
# plt.axvline(x=f_RED, color='r', linestyle='-')
# plt.axvline(x=f_BLUE, color='b', linestyle='-')
# plt.show()


# ellenörzés napállandóval
B=2*h*f**3 /( c**2*(np.exp(h*f/k_B/T)-1) ) #[J*sec*m^2/sec^2/m^5] = [J/sec/m^3]
A_S=4*R_S**2*np.pi
A_T=4*R_T**2*np.pi
print(f'Suns surface Area =\t\t\t\033[1m{A_S:.2E} m^2\033[0m')
P_plnk=np.sum(B*1e13)*A_S*np.pi #itt nem kell 4-es szorzó, mert Lambert felület
P_stp=A_S*sigma*T**4
print(f'output according to Plank:\t\t\033[1m{P_plnk:.2E} W\033[0m')
print(f'outut of the sun according to Stephan:\t\033[1m{P_stp:.2E} W\033[0m')
S=P_plnk/A_T #[W/m^2]
print(f'Napállandó=\t\t\t\t\033[1m{S:.2f} W/m^2\033[0m')