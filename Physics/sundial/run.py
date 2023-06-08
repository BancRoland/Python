import numpy as np
import matplotlib.pyplot as plt
import math

T0=100      #tavaszi napéjegyenlőség óta eltelt idő

sd=47       #adott szélességi kör
phi_d=23.5  #tengelyferdeség

T0=np.arange(3,10,1) 
Tl=365/12*T0

for T0 in Tl:
    phi=phi_d/180*math.pi
    T=T0*2*math.pi/365

    s=sd/180*math.pi
    a=np.arcsin(np.sin(phi)*np.sin(T))

    t0=np.arange(0,24,1)
    t=(t0-12+1e-3)*2*math.pi/24

    c=np.arccos(np.sin(a)*np.sin(s)+np.cos(a)*np.cos(s)*np.cos(t))
    elev=math.pi/2-c
    azmt=math.pi+np.sign(np.sin(t))*(math.pi-np.arccos((np.sin(a)-np.sin(s)*np.cos(c))/np.cos(s)/np.sin(c)))
    shadow=1/np.tan(elev)

    # plt.plot(t,azmt,'.-')
    # plt.plot(t,elev,'.-')
    # plt.plot(t,shadow,'.-')
    # plt.ylim([-5,10])
    # plt.grid()
    # plt.show()

    plt.polar(azmt,(shadow),'.-')
plt.ylim([0,10])
plt.grid(True)
plt.legend(['jún.21','júl.21','aug.21','sept.21','okt.21','nov.21', 'dec.21'])
plt.show()
plt.savefig('books_read.png')