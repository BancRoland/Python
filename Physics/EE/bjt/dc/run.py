import matplotlib.pyplot as plt
import numpy as np

U_BE = 0.7   #[V]
beta = 100

U = 5       #[V]

R1 = 15e3   #[Ohm]
R2 = 10e3   #[Ohm]
R3 = 1e3    #[Ohm]
R4 = 1e3    #[Ohm]

r5 = R2 / ( R1 + R2 )

I = ( r5 * U - U_BE ) / ( r5*R1 + R4*( beta + 1 ) )

phi1 = U_BE + R4 * I * ( beta + 1 )

U_ki2 = R4*I*(beta+1)
U_ki1 = U - R3*I*beta

print(U_ki1)








pot = 10e3  #[Ohm]
r = np.arange(100)/100

U_BE = 0.7   #[V]
beta = 100

U = 5       #[V]

R1 = np.arange(0,100)*1e3   #[Ohm]
R2 = 10e3   #[Ohm]
R3 = 1e3    #[Ohm]
R4 = 10    #[Ohm]

r5 = R2 / ( R1 + R2 )

I = ( r5 * U - U_BE ) / ( r5*R1 + R4*( beta + 1 ) )

phi1 = U_BE + R4 * I * ( beta + 1 )

U_ki2 = R4*I*(beta+1)
U_ki1 = U - R3*I*beta

# plt.plot(phi1)
# plt.plot(I*1e3)
# plt.ylabel("U_ki output voltage [V]")
# plt.xlabel("10k potentiometer position []")
# plt.grid()
# plt.show()



beta = 100

U = 3       #[V]

R1 = 100e3   #[Ohm]
R2 = 50e3   #[Ohm]
R3 = 1e3    #[Ohm]
R4 = 1    #[Ohm]

r5 = R2 / ( R1 + R2 )
Ube = np.arange(0,1,0.001)
beta = 100
I0 = 1e-13 #[A] záróirányú telítési áram
k = 1.38e-23    #[m2 kg s-2 K-1]
T = 300     #[K]
q = 96500/6e23  #[C] charge of one electron
U_T = k*T / q
I_E = (beta+1)*I0*(np.exp(Ube/U_T)-1)
I_2 = (beta+1)*( r5 * U - Ube ) / ( r5*R1 + R4*( beta + 1 ) )

x=np.argmin(abs(R3*(I_2-I_E)))
U_C = U-R3*I_E[x]
I_E0 = I_E[x]

print(x)
print(f"U_BE    =   {Ube[x]:.3f} V")
print(f"U_C     =   {U_C:.3f} V")
print(f"I_E0    =   {1e3*I_E0:.3f} mA")

rd = U_T/I_E0
rd_0 = (Ube[x+1]-Ube[x])/(I_E[x+1]-I_E[x])

print(f"rd      =   {rd:.3f} Ohm    ~   {rd_0:.3f} Ohm")

A = R3*beta/(rd+R4)/(beta+1)

rd2 = (rd+R4)*(beta+1)
r_in = (R1**-1+R2**-1+rd2**-1)**-1
r_out = R3

print(f"A       =   {A:.3f}")
print(f"r_in    =   {r_in:.3f}")
print(f"r_out   =   {r_out:.3f}")

print(U_T)

if(0):
    plt.plot(Ube,I_E)
    plt.plot(Ube,I_2)
    plt.ylim([-0.1,1])
    plt.grid()
    plt.ylabel("emitter current [A]")
    plt.xlabel("Base-Emitter voltage [V]")
    plt.title("transphere characteristic on 300 K with 1nA drift current")
    plt.show()



plt.plot(Ube,U-R3*I_E,".-")
plt.plot(Ube,U-R3*I_2,".-")
plt.ylim([-0.1*U,1.1*U])
plt.axhline(U,linestyle="--",color="gray",alpha=0.8)
plt.axhline(0,linestyle="--",color="gray",alpha=0.8)
plt.axhline(U/2,linestyle="--",color="gray",alpha=0.8)
plt.grid()
plt.ylabel("collector volage [V]")
plt.xlabel("Base-Emitter voltage [V]")
plt.title("transphere characteristic on 300 K with 1nA drift current")
plt.show()

