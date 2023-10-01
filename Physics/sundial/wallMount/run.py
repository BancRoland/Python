import numpy as np
import matplotlib.pyplot as plt
import math
import datetime

latest_equinox_date = datetime.datetime(2023, 3, 20)
current_time = datetime.datetime.now()
Diff=current_time-latest_equinox_date
# print(Diff.days)

# Get the current hour as a formatted string
hour = current_time.hour
min = current_time.minute
sec = current_time.second
days=Diff.days
print(f'days=   {days}')
# days=365.25/2   
# hour=15
# min=30
# sec=0

# days=3*365/4

hour=(hour-1)+min/60+sec/60/60


T0=100      #tavaszi napéjegyenlőség óta eltelt idő
sd=47.208       #adott szélességi kör
phi_d=23.44  #tengelyferdeség
alpha=90
# T00=np.arange(1,12,1)
T00=np.array([3, 6, 9])
# T00=np.array([0])
Tl=365.25/12*T00

# plt.figure(figsize=(10, 8))
for T0 in Tl:
    phi=phi_d/180*math.pi
    T=T0*2*math.pi/365

    s=sd/180*math.pi
    a=np.arcsin(np.sin(phi)*np.sin(T))

    t0=np.arange(0,25,1)  #dél óta eltelt idő
    t=(t0-12)*2*math.pi/24

    c=np.arccos(np.sin(a)*np.sin(s)+np.cos(a)*np.cos(s)*np.cos(t))
    elev0=math.pi/2-c
    azmt0=-(alpha-90)/180*np.pi+math.pi+np.sign(np.sin(t))*(math.pi-np.arccos((np.sin(a)-np.sin(s)*np.cos(c))/np.cos(s)/np.sin(c)))
    shadow0=1/np.tan(elev0)
    shadow=[]
    azmt=[]
    elev=[]
    for s in range(len(azmt0)):
        # if (azmt0[s] > alpha/180*np.pi and azmt0[s] < (alpha+180)/180*np.pi) and elev0[s] > 0 :
        if 1 :
            shadow=np.concatenate([shadow, [shadow0[s]]])
            azmt=np.concatenate([azmt, [azmt0[s]]])
            elev=np.concatenate([elev, [elev0[s]]])
    # plt.grid()
    # C=shadow*np.exp(1j*(-azmt-math.pi/2))
    # plt.plot(np.real(C),np.imag(C),color="C0",alpha=0.8)
    
    H=1/np.tan(azmt-np.pi/2)
    V=-np.tan(elev)*np.sqrt(1+H**2)

    print(f"len(H)={len(H)}")
    print(f"len(V)={len(V)}")
    print(f"{np.array(str(t))}")

    # plt.plot(-H,V,'o-',color="C0",alpha=0.8)
    # for k in range(len(t)):
    #     plt.text(-H[k],V[k],f"{t[k]*24/2/np.pi:.2f}")

    plt.subplot(2,1,1)
    plt.plot(t0,azmt/np.pi*180,'o-')
    plt.axhline(90)
    plt.axhline(270)
    plt.grid()
    plt.xlabel("hour")
    plt.ylabel("Azimuth [deg]")
    # plt.xlim([np.pi/2,3*np.pi/2])
    plt.subplot(2,1,2)
    plt.plot(t0,elev/np.pi*180,'o-')
    plt.axhline(0)
    plt.grid()
    plt.xlabel("hour")
    plt.ylabel("Elevaion [deg]")
    # plt.xlim([np.pi/2,3*np.pi/2])
# plt.xlim([np.pi,3*np.pi])
# plt.ylim([-3,0])
plt.show()

# # txt=["VI","VII","VIII","IX","X","XI","XII","I","II","III","IIII","V","VI","VII","VIII","IX","X","XI","XII","I","II","III","IIII","V"]
# txt=["VI","  V","IIII","III","II","I","XII","XI","X","IX","VIII","VII   ","VI","V","IIII","","","","","","","","VIII","VII"]

# Cc=5*np.exp(1j*((alpha-90)/180*np.pi+np.arange(0,4*math.pi,2*math.pi/24)))
# plt.plot(np.real(Cc),1/np.sin(sd/180*math.pi)*np.imag(Cc)-1/np.tan(sd/180*math.pi),'.-',color="C3",alpha=0.5)
# plt.gca().set_aspect('equal')

# for i in range(24):
#     plt.plot([0,np.real(100*Cc[i])],[-1/np.tan(sd/180*math.pi),1/np.sin(sd/180*math.pi)*np.imag(100*Cc[i])-1/np.tan(sd/180*math.pi)],'-',color="gray",alpha=0.5)
#     plt.text(1.2*np.real(Cc[i]), 1.1*1/np.sin(sd/180*math.pi)*np.imag(Cc[i])-1/np.tan(sd/180*math.pi), txt[i], fontsize=12, ha='center', va='center', fontweight='bold')


# # for T0 in Tl:
# #     phi=phi_d/180*math.pi
# #     T=T0*2*math.pi/365

# #     s=sd/180*math.pi
# #     a=np.arcsin(np.sin(phi)*np.sin(T))
    
# #     # # t0=np.arange(0,25,1)
# #     # t0=np.array([11,12,13,14])
# #     t0=np.arange(1,24,1)
# #     # t0=np.concatenate([[1e-8],t0,[24-1e8]])
# #     t=(t0-12)*2*math.pi/24
# #     c=np.arccos(np.sin(a)*np.sin(s)+np.cos(a)*np.cos(s)*np.cos(t))
# #     elev=math.pi/2-c
# #     azmt=math.pi+np.sign(np.sin(t))*(math.pi-np.arccos((np.sin(a)-np.sin(s)*np.cos(c))/np.cos(s)/np.sin(c)))
# #     shadow=1/np.tan(elev)
# #     # plt.polar(-azmt-math.pi/2,(shadow),'.',alpha=0.5,color="gray")
# #     C=shadow*np.exp(1j*(-azmt-math.pi/2))
# #     plt.plot(np.real(C),np.imag(C),'.',color="gray",alpha=0.5)


# phi=phi_d/180*math.pi
# # T=Diff.days*2*math.pi/365
# T=days*2*math.pi/365
# s=sd/180*math.pi
# a=np.arcsin(np.sin(phi)*np.sin(T))
# t0=np.arange(0,24,1)
# t=(t0-12)*2*math.pi/24
# c=np.arccos(np.sin(a)*np.sin(s)+np.cos(a)*np.cos(s)*np.cos(t))
# elev=math.pi/2-c
# azmt0=-(alpha-90)/180*np.pi+math.pi+np.sign(np.sin(t))*(math.pi-np.arccos((np.sin(a)-np.sin(s)*np.cos(c))/np.cos(s)/np.sin(c)))
# shadow0=1/np.tan(elev)
# # plt.polar(-azmt-math.pi/2,(shadow),'--',color="gray",alpha=0.5)
# shadow=[]
# azmt=[]
# for s in range(len(shadow0)):
#     if shadow0[s] > 0 :
#         shadow=np.concatenate([shadow, [shadow0[s]]])
#         azmt=np.concatenate([azmt, [azmt0[s]]])
# C=shadow*np.exp(1j*(-azmt-math.pi/2))
# plt.plot(np.real(C),np.imag(C),'--',color="gray",alpha=0.5)

# T=days*2*math.pi/365
# s=sd/180*math.pi
# a=np.arcsin(np.sin(phi)*np.sin(T))
# t0=hour
# t=(t0-12+1e-3)*2*math.pi/24
# c=np.arccos(np.sin(a)*np.sin(s)+np.cos(a)*np.cos(s)*np.cos(t))
# elev=math.pi/2-c
# azmt=math.pi+np.sign(np.sin(t))*(math.pi-np.arccos((np.sin(a)-np.sin(s)*np.cos(c))/np.cos(s)/np.sin(c)))
# shadow=1/np.tan(elev)
# if shadow>0:
#     C=shadow*np.exp(1j*(-azmt-math.pi/2))
#     plt.plot([0,np.real(C)],[-1/np.tan(sd/180*math.pi),np.imag(C)],'-',color="black",linewidth=3)
#     # plt.plot([-math.pi/2,-azmt-math.pi/2],[1/np.tan(sd/180*math.pi),shadow],'-',color="black")
# else:
#     plt.text(0, 4.5, "IT IS NIGHT", fontsize=12, ha='center', va='center', fontweight='bold')

# # plt.grid(True)
# plt.scatter(0,-1/np.tan(sd/180*math.pi),color="black")

# plt.xlim([-7.5,7.5])
# plt.ylim([-5,7.5])

# # # plt.legend(['jún.21','júl.21','aug.21','sept.21','okt.21','nov.21', 'dec.21'])
# plt.savefig('output.png', dpi=100)  # Adjust the file format and filename as needed
# plt.show()
