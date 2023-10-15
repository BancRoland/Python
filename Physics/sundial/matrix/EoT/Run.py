from sqlite3 import Date
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sys

from matplotlib.font_manager import FontProperties
import matplotlib.font_manager
import os

# Get the home directory of the current user
home_directory = os.path.expanduser("~")
sys.path.append(home_directory+"/Desktop/Python/math/matrices/Rodrigues_rot")

import banc_vectorManip as vMp

# from Rodrigues_rot import banc_vectorManip

# matplotlib.font_manager.findSystemFonts(fontpaths=None, fontext='ttf')
# font = FontProperties()
# font.set_family('serif')
# font.set_name('Times New Roman')

Y_sol=365.2422*24   #[hour]
D_sol=24
D_sid=1/(1/D_sol+1/Y_sol)
YEAR=2030

axialTilt=23.5047   # [deg] around x axis

GeoLat=47.19961979580085    # [deg]
GeoLon=18.401830866143445   # [deg]
GMT=1

# GeoLat=90    # [deg]
# GeoLon=0   # [dege]
# GMT=0

x=np.array([1,0,0])
y=np.array([0,1,0])
z=np.array([0,0,1])
O=np.array([0,0,0])
RotAx=vMp.rotX(z,23.5/180*np.pi)


def eclipticCoord(t):   #t: [sec]   secounds passed since spring equinox
    S=vMp.rotZ(np.array([1,0,0]),t/86400*D_sol/Y_sol*2*np.pi)
    return S


def eclip2eqat(v):
    S=vMp.rotX(v,23.5/180*np.pi)
    return S


def equatRot(t,v):
    S=vMp.rotZ(v,-(((t/86400/D_sid)*D_sol)*2*np.pi))
    return S


def equat2horiz(v,GeoLat):  #GeoLat [deg]
    S=vMp.rotY(v,(90-GeoLat)/180*np.pi) #X irányba van észak
    return S


def getHoriz(t,GeoLat):     #[sec]
    eqV=getEquat(t)
    eqV2=equatRot(t,eqV)
    horiz=equat2horiz(eqV2,GeoLat)
    return horiz


def horizOfDate(D,GeoLat,H):    #[year rat 0-1] [deg] [hour]
    S=vMp.rotZ(np.array([1,0,0]),D*2*np.pi)
    S=vMp.rotX(S,23.5/180*np.pi)
    S=vMp.rotZ(S,-((D+H/D_sol)*2*np.pi))
    S=vMp.rotY(S,(90-GeoLat)/180*np.pi) #X irányba van észak
    return S


def middleSun(D):   #sec
    D=D/86400/365.25
    return vMp.rotZ(x,D*2*np.pi)


def getEquat(t):    #[sec]
    ecV=eclipticCoord(t)
    eqV=eclip2eqat(ecV)
    return eqV
    

def FindZero():
    Days=np.arange(70,90,0.01)
    for d in Days:
        D=6.24004077+0.01720197*(365.25*(YEAR-2000)+d)
        H=9.863*np.sin(2*D+3.5932)
        if H >=0:
            return d


def TimeEq0():
    delta_t=[]
    harm1=[]
    harm2=[]
    Days=np.arange(0,365)
    for d in Days:
        D=6.24004077+0.01720197*(365.25*(YEAR-2000)+d)
        delta_t.append(-7.658*np.sin(D)+9.863*np.sin(2*D+3.5932))
        harm1.append(-7.658*np.sin(D))
        harm2.append(9.863*np.sin(2*D+3.5932))
    harm1=np.array(harm1)*60/86400*2*np.pi
    harm2=np.array(harm2)*60/86400*2*np.pi
    plt.plot(harm1)
    plt.plot(harm2)
    plt.plot(np.array(harm1)+np.array(harm2))
    plt.grid()
    plt.xlabel("time since spring eq [days]")
    plt.ylabel("diff in Retascence [Rad]")
    plt.title("Difference in rectascence between actual sun and fictive equatorial middlesun")
    plt.show()



def getEquatEoT(t): #[sec]
    d=t/86400
    D=6.24004077+0.01720197*(365.25*(YEAR-2000)+d+FindZero())
    delta_t=(-7.658*np.sin(D)+9.863*np.sin(2*D+3.5932))

    delta_t=np.array(delta_t)/60/24*np.pi*2
    
    v=middleSun(t)
    v=vMp.rotZ(v,delta_t)
    v=vMp.LPitrsect(RotAx,O,z,v)
    v=vMp.norm(v)

    return v


def getHoriz_EoT(t,GeoLat): #[sec]
    eqV=getEquatEoT(t)
    eqV2=equatRot(t,eqV)
    horiz=equat2horiz(eqV2,GeoLat)
    return horiz



def TimeEq_EoT():
    G=[]
    EoT_x=[]
    EoT_y=[]
    EoT_z=[]
    MS_x=[]
    MS_y=[]
    MS_z=[]
    delta_t=[]
    for Days in np.arange(0,366,7):

        EoT=getEquatEoT(Days*86400)
        # EoT=getEquat(Days*86400)
        EoT[2]=0
        EoT_x.append(EoT[0])
        EoT_y.append(EoT[1])
        EoT_z.append(EoT[2])

        MS=middleSun(Days*86400)
        MS_x.append(MS[0])
        MS_y.append(MS[1])
        MS_z.append(MS[2])

        g=vMp.XY_plane_angleDiff(EoT,MS)/2/np.pi*24*60

        D=6.24004077+0.01720197*(365.25*(YEAR-2000)+Days+FindZero())
        delta_t.append(-7.658*np.sin(D)+9.863*np.sin(2*D+3.5932))

        G.append(g)

    G=np.array(G)
    delta_t=np.array(delta_t)
    plt.plot(G,"o")
    plt.plot(delta_t)
    plt.grid()
    plt.ylabel("min")
    plt.xlabel("week")
    plt.title("Ennyivel siet a napóra a helyi középidőhöz képest")
    plt.legend(["szimuláció","egyenlet alapján"])
    plt.show()




HourDiff=GeoLon/360*24-GMT

WallAzmt=157    # [deg], right side is free
# WallAzmt=90    # [deg], right side is free
xlim=[-3,2.5]
ylim=[-6,3]
# xlim=[-0.5,0.5]
# ylim=[-0.5,0.5]





# # horizontal plane
# P=np.array([0,0,0])
# n=np.array([0,0,1])
# L=np.array([0,0,1])


# vertical wall with given azmt direction, rigth side is free
azmt=WallAzmt/180*np.pi
# azmt=90/180*np.pi
nWall=vMp.ROT(-y,z,-azmt)


A=np.array([np.cos(axialTilt/180*np.pi),0,np.sin(axialTilt/180*np.pi)])
Dates=[0,np.pi/2,np.pi,np.pi/2*3]
Hours=np.arange(0,2*np.pi,2*np.pi/24)


TimeEq_EoT()    #ellenőrzésnek, hogy megfelelő-e az időegyenlet implementálása



plt.figure(figsize=(5, 8), dpi=100)

#for analemmas with EoT
Hours=np.arange(12,20)
Dates=np.arange(0,365,7)
for H in Hours:
    H=H+HourDiff
    Vx=[]
    Vy=[]
    Vz=[]
    Vx2=[]
    Vy2=[]
    Vz2=[]
    for D in Dates:
        # S3=getHoriz(D*86400+H*60*60,GeoLat)
        S=getHoriz_EoT(D*86400+H*60*60,GeoLat)

        I=vMp.LPitrsect(nWall,O,S,nWall)
        I=vMp.rotZ(I,azmt-np.pi/2)
        I=vMp.rotY(I,np.pi/2)

        if np.dot(nWall,S)>0:
            if np.dot(z,S)>=0:
                Vx.append(I[0])
                Vy.append(I[1])
                Vz.append(I[2])
            else:
                Vx2.append(I[0])
                Vy2.append(I[1])
                Vz2.append(I[2])

    if len(Vx)>0:
        plt.plot(np.multiply(-1,Vy), Vx, color="black", alpha=0.8, linestyle='-')
    if len(Vx2)>0:
        plt.plot(np.multiply(-1,Vy2), Vx2, color="black", alpha=0.2, linestyle='-')


# #for analemmas without EoT
# Hours=np.arange(12,20)
# Dates=np.arange(0,365,7)
# for H in Hours:
#     H=H+HourDiff
#     Vx=[]
#     Vy=[]
#     Vz=[]
#     for D in Dates:
#         S3=getHoriz(D*86400+H*60*60,GeoLat)
#         # S3=getHoriz_EoT(D*86400+H*60*60,GeoLat)

#         I=vMp.LPitrsect(nWall,O,S3,nWall)
#         I=vMp.rotZ(I,azmt-np.pi/2)
#         I=vMp.rotY(I,np.pi/2)

#         if np.dot(nWall,S3)>0:
#             Vx.append(I[0])
#             Vy.append(I[1])
#             Vz.append(I[2])
#     if len(Vx)>0:
#         plt.plot(np.multiply(-1,Vy), Vx, color="black", alpha=0.2, linewidth=1)


# # For single point
# H=12
# D=0
# H=H+HourDiff
# # S=getHoriz(D*86400+H*60*60,GeoLat)
# # S=horizOfDate(D, GeoLat, H)
# S=getHoriz_EoT(D*86400+H*60*60,GeoLat)
# I=vMp.LPitrsect(nWall,O,S,nWall)
# I=vMp.rotZ(I,azmt-np.pi/2)
# I=vMp.rotY(I,np.pi/2)
# if np.dot(nWall,S)>0:
#     plt.scatter(np.multiply(-1,I[1]), I[0], color="red", alpha=0.8, marker="o")

# For dotted lines of extremes
Hours=np.arange(0,24,0.1)
Dates=np.array([0,1/4,3/4])
for D in Dates:
    Vx=[]
    Vy=[]
    Vz=[]
    Vx2=[]
    Vy2=[]
    Vz2=[]
    for H in Hours:
        H=H+HourDiff
        S=horizOfDate(D, GeoLat, H)
        I=vMp.LPitrsect(nWall,O,S,nWall)
        I=vMp.rotZ(I,azmt-np.pi/2)
        I=vMp.rotY(I,np.pi/2)

        if np.dot(nWall,S)>0:
            if np.dot(z,S)>=0:
                Vx.append(I[0])
                Vy.append(I[1])
                Vz.append(I[2])
            else:
                Vx2.append(I[0])
                Vy2.append(I[1])
                Vz2.append(I[2])

    if len(Vx)>0:
        plt.plot(np.multiply(-1,Vy), Vx, color="black", alpha=0.8, linestyle='--')
    if len(Vx2)>0:
        plt.plot(np.multiply(-1,Vy2), Vx2, color="black", alpha=0.2, linestyle='--')


#for numbers of hours
NP=vMp.rotY(z,(90-GeoLat)/180*np.pi)
polarIntersect=vMp.LPitrsect(nWall,O,NP,nWall)
polarIntersect=vMp.rotZ(polarIntersect,azmt-np.pi/2)
polarIntersect=vMp.rotY(polarIntersect,np.pi/2)

plt.scatter(np.multiply(-1,polarIntersect[1]), polarIntersect[0], color="black", alpha=0.8, marker=".")
plt.scatter(0, 0, color="black", alpha=0.8, marker="o")

Hours=np.arange(12,20)
Hours_Labels=["XII","I","II","III","IIII","V","VI","VII","VIII","IX","X","XI","XII","I","II","III","IIII","V","VI","VII","VIII","IX","X","XI"]
# Dates=np.array([1/4])
# for D in Dates:
D=1/4
D2=3/4
Vx=[]
Vy=[]
for h in Hours:
    H=h+HourDiff
    S=horizOfDate(D, GeoLat, H)
    I=vMp.LPitrsect(nWall,O,S,nWall)
    I=vMp.rotZ(I,azmt-np.pi/2)
    I=vMp.rotY(I,np.pi/2)

    S2=horizOfDate(D2, GeoLat, H)
    I2=vMp.LPitrsect(nWall,O,S2,nWall)
    I2=vMp.rotZ(I2,azmt-np.pi/2)
    I2=vMp.rotY(I2,np.pi/2)
    
    I_N0=polarIntersect+1.1*(I-polarIntersect)
    I_N1=polarIntersect+1.05*(I_N0-polarIntersect)
    
    if np.dot(nWall,S)>0:
        plt.text(-1*I_N1[1], I_N1[0], Hours_Labels[h], horizontalalignment='center', verticalalignment='center', size=8, weight="bold", font="serif")
                
        Vx=np.zeros(2)
        Vx[0]=I2[0]
        Vx[1]=polarIntersect[0]

        Vy=np.zeros(2)
        Vy[0]=I2[1]
        Vy[1]=polarIntersect[1]
        plt.plot(np.multiply(-1,Vy), np.multiply(1,Vx), color="black", alpha=0.2, linestyle='-')


        Vx=np.zeros(2)
        Vx[0]=I[0]
        Vx[1]=I_N0[0]

        Vy=np.zeros(2)
        Vy[0]=I[1]
        Vy[1]=I_N0[1]
        plt.plot(np.multiply(-1,Vy), np.multiply(1,Vx), color="black", alpha=0.2, linestyle='-')




#for analemma directions
Hours=np.array([12])
Dates=np.arange(0,365,7)
for H in Hours:
    H=H+HourDiff
    Vx=[]
    Vy=[]
    Vz=[]
    for D in Dates:
        # S3=getHoriz(D*86400+H*60*60,GeoLat)
        S3=getHoriz_EoT(D*86400+H*60*60,GeoLat)

        I=vMp.LPitrsect(nWall,O,S3,nWall)
        I=vMp.rotZ(I,azmt-np.pi/2)
        I=vMp.rotY(I,np.pi/2)

        if np.dot(nWall,S3)>0:
            Vx.append(I[0])
            Vy.append(I[1])
            Vz.append(I[2])
    if len(Vx)>0:
        # plt.plot(np.multiply(-1,Vy), Vx, color="black", alpha=0.2)
        for i in [5,19,30,46]:
            plt.quiver(-Vy[i],Vx[i],-Vy[i+1]+Vy[i],Vx[i+1]-Vx[i])



plt.xlim(xlim)
plt.ylim(ylim)

plt.plot([-10, 10],[0,0],':',alpha=0.3, color="black")
plt.plot([np.multiply(-1,polarIntersect[1]), np.multiply(-1,polarIntersect[1])],[-10, 10],':',alpha=0.3, color="black")

# plt.grid()
plt.gca().set_aspect('equal')
plt.text(0.99*xlim[1],0.99*ylim[0],f"GMT +{GMT}\nLon: {GeoLon:.3f}\nLat: {GeoLat:.3f}\nwAZMT: {WallAzmt:.0f}˚", horizontalalignment='right', verticalalignment='bottom', size=8)
# plt.grid()
plt.savefig("map.png")
plt.show()