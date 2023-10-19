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

#Horiz
# X -> észak
# Y -> nyugat
# Z -> fel

#Equat
# X -> tavaszpont
# Y -> égi felső kulmináció


Y_sol=365.2422*24   #[hour]
D_sol=24
D_sid=1/(1/D_sol+1/Y_sol)
YEAR=2030
Y_sec=365.2422*86400   #[hour]

axialTilt=23.5047   # [deg] around x axis

GeoLat=47.19961979580085    # [deg]
GeoLon=18.401830866143445   # [deg]
# GeoLat=51.48    # [deg]
# GeoLon=-0.0015   # [deg]
GMT=1
ToSE= (78+22/24+24/60/24)*86400  #[sec] 2023. 03. 20. 22:24

WallAzmt=157    # [deg], right side is free
# WallAzmt=90    # [deg], right side is free

WallInc=0   #[deg] angle realtive to vertcal. 90 is horizontal flat

xlim=[-3,2.5]
ylim=[-6,3]
# xlim=[-5,5]
# ylim=[-5,5]

# GeoLat=90    # [deg]
# GeoLon=0   # [dege]
# GMT=0

x=np.array([1,0,0])
y=np.array([0,1,0])
z=np.array([0,0,1])
O=np.array([0,0,0])
# RotAx=vMp.rotX(z,axialTilt/180*np.pi) #UPDATED later


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

def getEclipticEoT(t): #[sec] time passed since jan. 1. 0:00
    d=t/86400
    D=6.24004077+0.01720197*(365.25*(YEAR-2000)+d)
    # D=0
    delta_t=(-7.658*np.sin(D)+9.863*np.sin(2*D+3.5932))

    delta_t=np.array(delta_t)/60/24*np.pi*2
    # print(f"delta_t= {delta_t}")

    v=middleSun(t)
    v=vMp.rotZ(v,-delta_t)

    return v


def FindEclipAx():
    A=getEclipticEoT(ToSE)
    angSE=vMp.XY_plane_angleDiff(A,x)
    print(f"equinox angle:{angSE/np.pi*180}")
    RotAx0=vMp.rotX(z,axialTilt/180*np.pi)
    print(f"RotAx0:  {RotAx0}")
    RotAx=vMp.rotZ(RotAx0,angSE)
    print(f"RotAx:  {RotAx}")
    return RotAx

RotAx=FindEclipAx()

def getEquatEoT(t): #[sec]
    v=getEclipticEoT(t)
    v=vMp.LPitrsect(RotAx,O,z,v)
    v=vMp.norm(v)

    return v

def getHoriz_EoT(t,GeoLat): #[sec]
    eqV=getEquatEoT(t)
    eqV2=equatRot(t,eqV)
    horiz=equat2horiz(eqV2,GeoLat)
    return horiz



def getEquatEoT0(t): #[sec]
    d=t/86400
    D=6.24004077+0.01720197*(365.25*(YEAR-2000)+d+FindZero())
    D=0
    delta_t=(-7.658*np.sin(D)+9.863*np.sin(2*D+3.5932))

    delta_t=np.array(delta_t)/60/24*np.pi*2
    # print(f"delta_t= {delta_t}")

    v=middleSun(t)
    v=vMp.rotZ(v,-delta_t)
    v=vMp.LPitrsect(RotAx,O,z,v)
    v=vMp.norm(v)

    return v

def getHoriz_EoT0(t,GeoLat): #[sec]
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

        g=vMp.XY_plane_angleDiff(MS,EoT)/2/np.pi*24*60

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

def horiz2AzEl(v):
    azmt=-np.arctan2(v[1],v[0])
    if azmt < 0:
        azmt=azmt+np.pi*2

    elev=np.arcsin(v[2])
    return azmt, elev

def analemmaCheck():
    GeoLat=51.48    # [deg]
    GeoLon=-0.0015   # [deg]
    GMT=0
    H=12
    azmtA=[]
    elevA=[]
    for D in np.arange(0,365):
        S=getHoriz_EoT(D*86400+H*60*60,GeoLat)
        # S=getHoriz(D*86400+H*60*60,GeoLat)
        azmt0,elev0=horiz2AzEl(S)
        azmtA.append(azmt0/np.pi*180)
        elevA.append(elev0/np.pi*180)
    plt.plot(azmtA,elevA,'r.',alpha=0.3)
    plt.plot([0, 366],[90-GeoLat,90-GeoLat],':',alpha=1, color="black")
    plt.plot([0, 366],[90-GeoLat+axialTilt,90-GeoLat+axialTilt],':',alpha=1, color="black")
    plt.plot([0, 366],[90-GeoLat-axialTilt,90-GeoLat-axialTilt],':',alpha=1, color="black")

    azmt=[]
    elev=[]
    # for D in [12,43,74,104,135,166,196,227,257,288,319,348]:
    texts=[" Jan 1"," Feb 1"," Mar 1"," Apr 1"," May 1"," Jun 1"," Jul 1"," Aug 1"," Sep 1"," Oct 1"," Nov 1"," Dec 1"]
    dates=[0,31,59,90,120,151,181,212,243,273,304,334]
    for Di in range(len(dates)):
        S=getHoriz_EoT((dates[Di])*86400+H*60*60,GeoLat)
        azmt0,elev0=horiz2AzEl(S)
        azmt.append(azmt0/np.pi*180)
        elev.append(elev0/np.pi*180)
        plt.text(azmt0/np.pi*180,elev0/np.pi*180,texts[Di])
    plt.plot(azmt,elev,'ko')

    azmtA=[]
    elevA=[]
    # for D in [0,91,182,274]:
    for D in [171,355,78,265]:
        S=getHoriz_EoT((D)*86400+H*60*60,GeoLat)
        # S=getHoriz((D)*86400+H*60*60,GeoLat)
        azmt0,elev0=horiz2AzEl(S)
        azmtA.append(azmt0/np.pi*180)
        elevA.append(elev0/np.pi*180)
    plt.plot(azmtA,elevA,'o',color=[0,1,0])

    plt.grid()
    plt.title("Horizontal position of the Sun at Greenwhich every day at 12:00")
    plt.xlabel("Azimuth[˚]")
    plt.ylabel("Altitude[˚]")
    plt.xlim([176,185])
    plt.ylim([0,70])
    plt.savefig("analemma.png")
    # plt.show()


HourDiff=GeoLon/360*24-GMT


# xlim=[-0.5,0.5]
# ylim=[-0.5,0.5]


# vertical wall with given azmt direction, rigth side is free
azmt=WallAzmt/180*np.pi
dep=WallInc/180*np.pi
# azmt=90/180*np.pi
nWall0=vMp.ROT(-y,x,-dep)
nWall=vMp.ROT(nWall0,z,-azmt)


A=np.array([np.cos(axialTilt/180*np.pi),0,np.sin(axialTilt/180*np.pi)])
Dates=[0,np.pi/2,np.pi,np.pi/2*3]
Hours=np.arange(0,2*np.pi,2*np.pi/24)


# TimeEq_EoT()    #ellenőrzésnek, hogy megfelelő-e az időegyenlet implementálása

analemmaCheck()

print(getEquatEoT(0))


plt.figure(figsize=(5, 8), dpi=100)

#for analemmas with EoT
Hours=np.arange(12,20)
Hours=np.array([12])
Dates=np.arange(0,365,1)
for H in Hours:
    H=H+HourDiff
    Vx=[]
    Vy=[]
    Vz=[]
    Vx2=[]
    Vy2=[]
    Vz2=[]
    for Dsomm in Dates:
        # S=getHoriz(D*86400+H*60*60,GeoLat)
        S=getHoriz_EoT(Dsomm*86400+H*60*60,GeoLat)

        I=vMp.LPitrsect(nWall,O,S,nWall)
        I=vMp.rotZ(I,azmt-np.pi/2)
        I=vMp.rotY(I,(np.pi/2-dep))

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
        # plt.plot(np.multiply(-1,Vy), Vx, ".", color="black", alpha=0.8)#, linestyle='o')
        plt.plot(np.multiply(-1,Vy), Vx, '.-', color="black", alpha=0.2)
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
#         I=vMp.rotY(I,(np.pi/2-dep))

#         if np.dot(nWall,S3)>0:
#             Vx.append(I[0])
#             Vy.append(I[1])
#             Vz.append(I[2])
#     if len(Vx)>0:
#         plt.plot(np.multiply(-1,Vy), Vx, color="black", alpha=0.2, linewidth=1)


# For single point
H=12
D0=[171,355,78,265]
H=H+HourDiff
# S=getHoriz(D*86400+H*60*60,GeoLat)
# S=horizOfDate(D, GeoLat, H)
for D in D0:
    S=getHoriz_EoT(D*86400+H*60*60,GeoLat)
    # S=getHoriz_EoT(ToSE,GeoLat)
    I=vMp.LPitrsect(nWall,O,S,nWall)
    I=vMp.rotZ(I,azmt-np.pi/2)
    I=vMp.rotY(I,(np.pi/2-dep))
    if np.dot(nWall,S)>0:
        plt.scatter(np.multiply(-1,I[1]), I[0], color="green", alpha=0.8, marker="o")



# For dotted lines of extremes
Hours=np.arange(0,24,0.1)
Dates=np.array([0,1/4,3/4])
for Dsomm in Dates:
    Vx=[]
    Vy=[]
    Vz=[]
    Vx2=[]
    Vy2=[]
    Vz2=[]
    for H in Hours:
        H=H+HourDiff
        S=horizOfDate(Dsomm, GeoLat, H)
        I=vMp.LPitrsect(nWall,O,S,nWall)
        I=vMp.rotZ(I,azmt-np.pi/2)
        I=vMp.rotY(I,(np.pi/2-dep))

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
polarIntersect=vMp.rotY(polarIntersect,(np.pi/2-dep))

plt.scatter(np.multiply(-1,polarIntersect[1]), polarIntersect[0], color="black", alpha=0.8, marker=".")
plt.scatter(0, 0, color="black", alpha=0.8, marker="o")

Hours=np.arange(12,20)
# Hours=np.array([13])
Hours_Labels=["XII","I","II","III","IIII","V","VI","VII","VIII","IX","X","XI","XII","I","II","III","IIII","V","VI","VII","VIII","IX","X","XI"]

Dsomm=1/4
Dwint=3/4
Vx=[]
Vy=[]
for h in Hours:
    H=h+HourDiff
    S=horizOfDate(Dsomm, GeoLat, H)
    I=vMp.LPitrsect(nWall,O,S,nWall)
    I=vMp.rotZ(I,azmt-np.pi/2)
    I=vMp.rotY(I,(np.pi/2-dep))

    S2=horizOfDate(Dwint, GeoLat, H)
    I2=vMp.LPitrsect(nWall,O,S2,nWall)
    I2=vMp.rotZ(I2,azmt-np.pi/2)
    I2=vMp.rotY(I2,(np.pi/2-dep))
    
    print(vMp.dist(polarIntersect,I))
    if vMp.dist(polarIntersect,I) > vMp.dist(polarIntersect,I2):
        Ia=I
        Ib=I2
    else:
        Ia=I2
        Ib=I

    I_N0=polarIntersect+1.1*(Ia-polarIntersect)
    I_N1=polarIntersect+1.05*(I_N0-polarIntersect)


    Vx=np.zeros(2)
    Vy=np.zeros(2)
    
    if np.dot(nWall,S2)>0:
        #távolbbi
        plt.text(-1*I_N1[1], I_N1[0], Hours_Labels[h], horizontalalignment='center', verticalalignment='center', size=8, weight="bold", font="serif")
        # plt.scatter(-1*I_N0[1], I_N0[0])        

        Vx[0]=Ib[0]
        Vx[1]=polarIntersect[0]

        Vy[0]=Ib[1]
        Vy[1]=polarIntersect[1]
        plt.plot(np.multiply(-1,Vy), np.multiply(1,Vx), color="black", alpha=0.2, linestyle='-')

    if np.dot(nWall,S)>0:
        Vx[0]=Ia[0]
        Vx[1]=I_N0[0]

        Vy[0]=Ia[1]
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
    for Dsomm in Dates:
        # S3=getHoriz(D*86400+H*60*60,GeoLat)
        S3=getHoriz_EoT(Dsomm*86400+H*60*60,GeoLat)

        I=vMp.LPitrsect(nWall,O,S3,nWall)
        I=vMp.rotZ(I,azmt-np.pi/2)
        I=vMp.rotY(I,(np.pi/2-dep))

        if np.dot(nWall,S3)>0:
            Vx.append(I[0])
            Vy.append(I[1])
            Vz.append(I[2])
    if len(Vx)>0:
        # plt.plot(np.multiply(-1,Vy), Vx, color="black", alpha=0.2)
        for i in [8,20,28,45]:
            plt.quiver(-Vy[i],Vx[i],-Vy[i+1]+Vy[i],Vx[i+1]-Vx[i])



plt.xlim(xlim)
plt.ylim(ylim)

plt.plot([-10, 10],[0,0],':',alpha=0.3, color="black")
plt.plot([np.multiply(-1,polarIntersect[1]), np.multiply(-1,polarIntersect[1])],[-10, 10],':',alpha=0.3, color="black")

# plt.grid()
plt.gca().set_aspect('equal')
plt.text(0.99*xlim[1],0.99*ylim[0],f"GMT +{GMT}\nLon: {GeoLon:.3f}\nLat: {GeoLat:.3f}\nwAZMT: {WallAzmt:.0f}˚\nwINC: {WallInc:.0f}˚", horizontalalignment='right', verticalalignment='bottom', size=8)
# plt.grid()
plt.savefig("map.png")
plt.show()