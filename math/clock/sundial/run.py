import numpy as np
import matplotlib.pyplot as plt
import math
import datetime

latest_equinox_date = datetime.datetime(2023, 3, 20)
current_time = datetime.datetime.now()
Diff=current_time-latest_equinox_date
print(Diff.days)

# Get the current hour as a formatted string
hour = current_time.hour
min = current_time.minute
sec = current_time.second
days=Diff.days
# hour=14
# min=0
# sec=0
# days=3*365/4

hour=hour+min/60+sec/60/60


T0=100      #tavaszi napéjegyenlőség óta eltelt idő

sd=47       #adott szélességi kör
phi_d=23.5  #tengelyferdeség

T0=np.arange(6,12,3)
print(T0)
# T0=np.array([3, 6, 9])
T0=np.array([9, 3, 6])
print(T0)
Tl=365/12*T0

for T0 in Tl:
    phi=phi_d/180*math.pi
    T=T0*2*math.pi/365

    s=sd/180*math.pi
    a=np.arcsin(np.sin(phi)*np.sin(T))

    # # t0=np.arange(0,25,1)
    # t0=np.array([11,12,13,14])
    t0=np.arange(1,24,0.1)
    # t0=np.concatenate([[1e-8],t0,[24-1e8]])
    t=(t0-12)*2*math.pi/24

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

    plt.polar(-azmt-math.pi/2,(shadow),'-',alpha=0.5)


for T0 in Tl:
    phi=phi_d/180*math.pi
    T=T0*2*math.pi/365

    s=sd/180*math.pi
    a=np.arcsin(np.sin(phi)*np.sin(T))
    
    # # t0=np.arange(0,25,1)
    # t0=np.array([11,12,13,14])
    t0=np.arange(1,24,1)
    # t0=np.concatenate([[1e-8],t0,[24-1e8]])
    t=(t0-12)*2*math.pi/24
    c=np.arccos(np.sin(a)*np.sin(s)+np.cos(a)*np.cos(s)*np.cos(t))
    elev=math.pi/2-c
    azmt=math.pi+np.sign(np.sin(t))*(math.pi-np.arccos((np.sin(a)-np.sin(s)*np.cos(c))/np.cos(s)/np.sin(c)))
    shadow=1/np.tan(elev)
    plt.polar(-azmt-math.pi/2,(shadow),'.',alpha=0.5,color="gray")


phi=phi_d/180*math.pi
# T=Diff.days*2*math.pi/365
T=days*2*math.pi/365
s=sd/180*math.pi
a=np.arcsin(np.sin(phi)*np.sin(T))
t0=np.arange(0,24,1)
t=(t0-12)*2*math.pi/24
c=np.arccos(np.sin(a)*np.sin(s)+np.cos(a)*np.cos(s)*np.cos(t))
elev=math.pi/2-c
azmt=math.pi+np.sign(np.sin(t))*(math.pi-np.arccos((np.sin(a)-np.sin(s)*np.cos(c))/np.cos(s)/np.sin(c)))
shadow=1/np.tan(elev)
plt.polar(-azmt-math.pi/2,(shadow),'--',color="gray",alpha=0.5)

T=days*2*math.pi/365
s=sd/180*math.pi
a=np.arcsin(np.sin(phi)*np.sin(T))
t0=hour
t=(t0-12+1e-3)*2*math.pi/24
c=np.arccos(np.sin(a)*np.sin(s)+np.cos(a)*np.cos(s)*np.cos(t))
elev=math.pi/2-c
azmt=math.pi+np.sign(np.sin(t))*(math.pi-np.arccos((np.sin(a)-np.sin(s)*np.cos(c))/np.cos(s)/np.sin(c)))
shadow=1/np.tan(elev)
plt.polar([-math.pi/2,-azmt-math.pi/2],[1/np.tan(sd/180*math.pi),shadow],'-',color="black")
plt.grid(True)
plt.scatter(0, 0,color="black")
# plt.scatter(-math.pi/2,1/np.tan(sd/180*math.pi),color="black")
print(1/np.tan(sd/180*math.pi))

plt.ylim([0,6])

# plt.legend(['jún.21','júl.21','aug.21','sept.21','okt.21','nov.21', 'dec.21'])
plt.savefig('books_read.png')
plt.show()
