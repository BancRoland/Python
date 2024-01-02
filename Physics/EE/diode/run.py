import matplotlib.pyplot as plt
import numpy as np

Ube = np.arange(0,1,0.01)
I0 = 1e-13 #[A] záróirányú telítési áram
k = 1.38e-23    #[m2 kg s-2 K-1]
T = 300     #[K]
q = 96500/6e23  #[C] charge of one electron
U_T = k*T / q
I = I0*(np.exp(Ube/U_T)-1)

print(U_T)

plt.plot(Ube,I)
plt.ylim([-0.1,1])
plt.grid()
plt.ylabel("diode current [A]")
plt.xlabel("diode voltage [V]")
plt.title("diode characteristic on 300 K with 1nA drift current")
plt.show()



for T in [250,300,350,400,450]:
    Ube = np.arange(0,1,0.01)
    I0 = 1e-13 #[A] drift current
    k = 1.38e-23    #[m2 kg s-2 K-1]
    # T = 300     #[K]
    q = 96500/6e23  #[C] charge of one electron
    U_T = k*T / q
    I = I0*(np.exp(Ube/U_T)-1)

    print(U_T)

    plt.plot(Ube,I,label=f"{T} K")
plt.ylim([-0.1,1])
plt.grid()
plt.ylabel("diode current [A]")
plt.xlabel("diode voltage [V]")
plt.legend()
plt.title("diode characteristic on different temperature with 1nA drift current")
plt.show()


