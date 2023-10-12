from sqlite3 import Date
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sys
sys.path.append("/home/roland/Desktop/Python/math/matrices/Rodrigues_rot")
import banc_vectorManip as vMp
from matplotlib.font_manager import FontProperties
import matplotlib.font_manager

# from Rodrigues_rot import banc_vectorManip

# matplotlib.font_manager.findSystemFonts(fontpaths=None, fontext='ttf')
# font = FontProperties()
# font.set_family('serif')
# font.set_name('Times New Roman')

Y_sol=365.2422*24   #[hour]
D_sol=24
D_sid=1/(1/D_sol+1/Y_sol)

    # S=vMp.rotZ(np.array([1,0,0]),D*D_sol/Y_sol*2*np.pi)
    # S=vMp.rotX(S,23.5/180*np.pi)
    # S=vMp.rotZ(S,-((D*D_sol/D_sid+H/D_sol)*2*np.pi))
    # S=vMp.rotY(S,(90-GeoLat)/180*np.pi) #X irányba van észak

    # # S=eclipticCoord(D*86400)
    # # S=eclip2eqat(S)
    # # S=equatRot(D*86400,S)
    # # S=equat2horiz(S,GeoLat)


def eclipticCoord(t):   #t: [sec]   secounds passed since spring equinox
    # v=np.array([1,0,0])
    # S=vMp.rotZ(v,D*D_sol/Y_sol*2*np.pi)
    # S=vMp.rotZ(v,(t/60/60)/Y_sol*2*np.pi)
    # S=vMp.rotZ(v,D*D_sol/Y_sol*2*np.pi)
    S=vMp.rotZ(np.array([1,0,0]),t/86400*D_sol/Y_sol*2*np.pi)
    return S

def eclip2eqat(v):
    S=vMp.rotX(v,23.5/180*np.pi)
    return S

def equatRot(t,v):
    # S=vMp.rotZ(v,-((D/86400*D_sol/D_sid+H/D_sol)*2*np.pi))
    S=vMp.rotZ(v,-(((t/86400/D_sid)*D_sol)*2*np.pi))
    # S=vMp.rotZ(v,-(((t/60/60)/D_sid+H/D_sol)*2*np.pi))
    return S

def equat2horiz(v,GeoLat):  #GeoLat [deg]
    S=vMp.rotY(v,(90-GeoLat)/180*np.pi) #X irányba van észak
    return S

def getHoriz(t,GeoLat):
    ecV=eclipticCoord(t)
    eqV=eclip2eqat(ecV)
    eqV2=equatRot(t,eqV)
    horiz=equat2horiz(eqV2,GeoLat)
    return horiz



axialTilt=23.5047   # [deg] around x axis

GeoLat=47.19961979580085    # [deg]
# GeoLon=18.401830866143445   # [deg]
# GMT=1

# GeoLat=90    # [deg]
GeoLon=0   # [deg]
GMT=0

HourDiff=GeoLon/360*24-GMT
print(HourDiff)



# WallAzmt=157    # [deg], right side is free
WallAzmt=90    # [deg], right side is free
# xlim=[-3,2.5]
# ylim=[-6,3]
xlim=[-10,10]
ylim=[-6,3]


x=np.array([1,0,0])
y=np.array([0,1,0])
z=np.array([0,0,1])


# # horizontal plane
# P=np.array([0,0,0])
# n=np.array([0,0,1])
# L=np.array([0,0,1])

# # South facing plane
# P=np.array([0,0,0])
# n=np.array([-1,0,0])
# L=np.array([-1,0,0])
# azmt=np.pi/2

# vertical wall with given azmt direction, rigth side is free
P=np.array([0,0,0])
azmt=WallAzmt/180*np.pi
# azmt=90/180*np.pi
n=vMp.ROT(np.array([0,-1,0]),np.array([0,0,-1]),azmt)
L=n


A=np.array([np.cos(axialTilt/180*np.pi),0,np.sin(axialTilt/180*np.pi)])
Dates=[0,np.pi/2,np.pi,np.pi/2*3]
Hours=np.arange(0,2*np.pi,2*np.pi/24)

# plt.figure(figsize=(8, 16))


#for analemmas
Hours=np.arange(4,20)
# Hours=np.array([12])
Dates=np.arange(0,365,7)
for H in Hours:
    H=H+HourDiff
    Vx=[]
    Vy=[]
    Vz=[]
    for D in Dates:
        # # S0=vMp.rotZ(np.array([1,0,0]),D*D_sol/Y_sol*2*np.pi)
        # # print(f"ecliptics:  {S0} {eclipticCoord(D*86400)}")
        # S0=eclipticCoord(D*86400)
        # print(f"S0={S0}")
        # # S1=vMp.rotX(S0,23.5/180*np.pi)
        # # print(f"equats: {S1} {eclip2eqat(S0)}")
        # S1=eclip2eqat(S0)
        # print(f"S1={S1}")
        # # S2=vMp.rotZ(S1,-((D*D_sol/D_sid+H/D_sol)*2*np.pi))
        # # print(f"days:   {S2} {equatRot(D,S1)}")
        # S2=equatRot((D*86400+H*60*60),S1)
        # print(f"S2={S2}")
        # # S3=vMp.rotY(S2,(90-GeoLat)/180*np.pi) #X irányba van észak
        # # print(f"horiz:  {S3} {equat2horiz(S2,GeoLat)}")
        # S3=equat2horiz(S2,GeoLat)
        # print(f"S3={S3}")
        
        S3=getHoriz(D*86400+H*60*60,GeoLat)


        I=vMp.LPitrsect(n,P,S3,L)

        # I=LayPlane(n,I)
        I=vMp.rotZ(I,azmt-np.pi/2)
        I=vMp.rotY(I,np.pi/2)

        if np.dot(n,S3)>0:
            Vx.append(I[0])
            Vy.append(I[1])
            Vz.append(I[2])
    if len(Vx)>0:
        plt.plot(np.multiply(-1,Vy), Vx, color="black", alpha=0.8)

#for dotted lines of extremes
Hours=np.arange(0,24,0.1)
Dates=np.array([0,1/4,2/4,3/4])
for D in Dates:
    Vx=[]
    Vy=[]
    Vz=[]
    for H in Hours:
        H=H+HourDiff
        # S=vMp.rotZ(np.array([1,0,0]),D*2*np.pi)
        # S=vMp.rotX(S,23.5/180*np.pi)
        # S=vMp.rotZ(S,-((D+H/D_sol)*2*np.pi))
        # S=vMp.rotY(S,(90-GeoLat)/180*np.pi) #X irányba van észak
        S=getHoriz(D*86400+H*60*60,GeoLat)
        I=vMp.LPitrsect(n,P,S,L)
        I=vMp.rotZ(I,azmt-np.pi/2)
        I=vMp.rotY(I,np.pi/2)

        

        if np.dot(n,S)>0:
            Vx.append(I[0])
            Vy.append(I[1])
            Vz.append(I[2])

    if len(Vx)>0:
        plt.plot(np.multiply(-1,Vy), Vx, color="black", alpha=0.8, linestyle='--')


#for numbers of hours
NP=vMp.rotY(z,(90-GeoLat)/180*np.pi)
polarIntersect=vMp.LPitrsect(n,P,NP,L)
polarIntersect=vMp.rotZ(polarIntersect,azmt-np.pi/2)
polarIntersect=vMp.rotY(polarIntersect,np.pi/2)

plt.scatter(np.multiply(-1,polarIntersect[1]), polarIntersect[0], color="black", alpha=0.8, marker=".")
plt.scatter(0, 0, color="black", alpha=0.8, marker="o")

Hours=np.arange(12,20)
Hours_Labels=["XII","I","II","III","IIII","V","VI","VII","VIII","IX","X","XI","XII","I","II","III","IIII","V","VI","VII","VIII","IX","X","XI"]
Dates=np.array([1/4,3/4])
for D in Dates:
    Vx=[]
    Vy=[]
    for h in range(len(Hours)):
        H=Hours[h]+HourDiff
        # S=vMp.rotZ(np.array([1,0,0]),D*2*np.pi)
        # S=vMp.rotX(S,23.5/180*np.pi)
        # S=vMp.rotZ(S,-((D+H/D_sol)*2*np.pi))
        # S=vMp.rotY(S,(90-GeoLat)/180*np.pi) #X irányba van észak, Y irányba nyugat
        S=getHoriz(D*86400+H*60*60,GeoLat)
        I=vMp.LPitrsect(n,P,S,L)
        I=vMp.rotZ(I,azmt-np.pi/2)
        I=vMp.rotY(I,np.pi/2)
        
        I=polarIntersect+1.1*(I-polarIntersect)
        I_N=polarIntersect+1.05*(I-polarIntersect)

        if np.dot(n,S)>0 and D==1/4:
            plt.text(-1*I_N[1], I_N[0], Hours_Labels[h], horizontalalignment='center', verticalalignment='center', size=12, weight="bold", font="serif")
                    
            Vx=np.zeros(2)
            Vx[0]=I[0]
            Vx[1]=polarIntersect[0]

            Vy=np.zeros(2)
            Vy[0]=I[1]
            Vy[1]=polarIntersect[1]
            plt.plot(np.multiply(-1,Vy), np.multiply(1,Vx), color="black", alpha=0.5, linestyle=':')

# plt.quiver(0,0,1,1)


# #for analemma direction
# Hours=np.arange(12,13)
# Dates=np.arange(0,365,7)
# for H in Hours:
#     H=H+HourDiff
#     Vx=[]
#     Vy=[]
#     Vz=[]
#     for D in Dates:
#         S=vMp.rotZ(np.array([1,0,0]),D*D_sol/Y_sol*2*np.pi)
#         S=vMp.rotX(S,23.5/180*np.pi)
#         S=vMp.rotZ(S,-((D*D_sol/D_sid+H/D_sol)*2*np.pi))
#         S=vMp.rotY(S,(90-GeoLon)/180*np.pi) #X irányba van észak
#         I=vMp.LPitrsect(n,P,S,L)

#         # I=LayPlane(n,I)
#         I=vMp.rotZ(I,azmt-np.pi/2)
#         I=vMp.rotY(I,np.pi/2)

#         if np.dot(n,S)>0 and np.dot(z,S)>0:
#             Vx.append(I[0])
#             Vy.append(I[1])
#             Vz.append(I[2])
#     if len(Vx)>0:
#         # plt.plot(np.multiply(-1,Vy), Vx, color="black", alpha=0.8)
#         for i in [5,19,30,46]:
#             plt.quiver(-Vy[i],Vx[i],-Vy[i+1]+Vy[i],Vx[i+1]-Vx[i])



plt.xlim(xlim)
plt.ylim(ylim)

plt.plot([-10, 10],[0,0],'--',alpha=0.5, color="black")
# plt.grid()
plt.gca().set_aspect('equal')
plt.text(xlim[1],ylim[0],f"Lon: {GeoLon:.3f}\nLat: {GeoLat:.3f}\nGMT +{GMT}", horizontalalignment='right', verticalalignment='bottom')
plt.grid()
plt.show()