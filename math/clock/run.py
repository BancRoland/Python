import numpy as np
import matplotlib.pyplot as plt
import math as m
import datetime

current_time = datetime.datetime.now()

# Get the current hour as a formatted string
hour = current_time.hour
min = current_time.minute
sec = current_time.second

print(hour)
print(min)
print(sec)

# hour=5
# min=45
# sec=50

min=min+sec/60
hour=hour+min/60+sec/60/60
O=0+0j

H=0.4*np.exp(-1j*(hour/12*2*m.pi-0.5*m.pi))
M=0.7*np.exp(-1j*(min/60*2*m.pi-0.5*m.pi))
S=0.9*np.exp(-1j*(sec/60*2*m.pi-0.5*m.pi))

perim=np.exp(2j*m.pi*np.arange(12+1)/12)
# for p in perim:
#     plt.scatter(np.real(p),np.imag(p))

txt=["XII","I","II","III","IIII","V","VI","VII","VIII","IX","X","XI"]
for i in range(12):
    pos=1.2*np.exp(1j*2*m.pi/12*i)
    plt.text(np.imag(pos), np.real(pos), txt[i], fontsize=12, ha='center', va='center')
plt.plot(np.imag(perim),np.real(perim),'o-',color="C0")
plt.scatter(np.real(O),np.imag(O),color="black")

# plt.scatter(np.real(H),np.imag(H))
plt.plot(np.real([O,H]),np.imag([O,H]),color="black",linewidth=5)
# plt.scatter(np.real(M),np.imag(M))
plt.plot(np.real([O,M]),np.imag([O,M]),color="black",linewidth=3)
# plt.scatter(np.real(S),np.imag(S))
plt.plot(np.real([O,S]),np.imag([O,S]),color="black",linewidth=1)
# plt.plot([np.real(np.concatenate([O[0],M[0]])),np.imag(np.concatenate([O[0],M[0]])])
plt.grid()
plt.xlim([-1.5,1.5])
plt.ylim([-1.5,1.5])
plt.gca().set_aspect('equal', adjustable='box')
plt.savefig("image.png")
plt.show()


