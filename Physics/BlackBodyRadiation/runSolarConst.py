import numpy as np
import matplotlib.pyplot as plt

T=6000
k_B=1.380649E-23 #[J/K] Boltzmann állandó
R_S=696_340_000 #[m] földtávolság
R_T=150E9 #[m] földtávolság
# f=10E12  #[Hz]    vizsgált frekvencia
f=np.arange(1e13,2e15,1e13)
f_RED=400e12
f_BLUE=790e12
c=3E8 #[m/s] speed of light
h=6.62607015E-34 #[J/Hz]
sigma=5.67E-8   #[W/m^2/K^4]

T0=range(1000,7000,1000)
lmbda=c/f

plt.plot()
for T in T0:
    B=2*h*c**2 /(lmbda**5 *(np.exp(h*c/lmbda/k_B/T)-1) )
    plt.plot(lmbda,B,'.-')
T=5778 #[K]
B=2*h*c**2 /(lmbda**5 *(np.exp(h*c/lmbda/k_B/T)-1) )
plt.plot(lmbda,B,'--')
plt.title("Planck sugárzási törvénye")
plt.grid()
plt.legend(T0)
plt.axvline(x=c/f_RED, color='r', linestyle='-')
plt.axvline(x=c/f_BLUE, color='b', linestyle='-')
plt.xlabel("hullámhossz [m]")
plt.ylabel("Intenzitás [W/m^2/srad]")
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


plt.plot()
for T in T0:
    B=2*h*f**3 /( c**2*(np.exp(h*f/k_B/T)-1) )
    plt.plot(f,B,'.-')
T=5778 #[K]
B=2*h*(f**3)/((c**2)*np.exp(h*f/k_B/T)-1)
plt.plot(f,B,'--')
plt.grid()
plt.legend(T0)
plt.axvline(x=f_RED, color='r', linestyle='-')
plt.axvline(x=f_BLUE, color='b', linestyle='-')
plt.xlabel("frekvencia [Hz]")
plt.ylabel("Intenzitás [W/m^2/srad]")
plt.show()

# ellenörzés napállandóval
T=5778 #[K]
B=2*h*f**3 /( c**2*(np.exp(h*f/k_B/T)-1) )
A_S=4*R_S**2*np.pi
A_T=4*R_T**2*np.pi
print(f'suns surface={A_S}')
P_plnk=np.sum(B*1e13)*A_S*np.pi #itt nem kell 4-es szorzó, mert Lambert felület
P_stp=A_S*sigma*T**4
print(f'output according to Plank {P_plnk}')
print(f'outut of the sun according to stephan {P_stp} ')
S=P_plnk/A_T
print(f'Napállandó= {S} W/m^2')