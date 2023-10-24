from sqlite3 import Date
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sys
import csv_read

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

EOT_TABLE=csv_read.getEOT_csv()


def eclipticCoord(t):   #t: [sec]   secounds passed since spring equinox
    S=vMp.rotZ(np.array([1,0,0]),t/86400*D_sol/Y_sol*2*np.pi)
    return S

def eclip2eqat(v):
    S=vMp.rotX(v,axialTilt/180*np.pi)
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
    S=vMp.rotX(S,axialTilt/180*np.pi)
    S=vMp.rotZ(S,-((D+H/D_sol)*2*np.pi))
    S=vMp.rotY(S,(90-GeoLat)/180*np.pi) #X irányba van észak
    return S

def middleSun(D):   #sec
    D=D/Y_sec
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

def getEoT_simple(t): #[sec] time passed since jan. 1. 0:00
    d=t/86400
    D=6.24004077+0.01720197*(365.25*(YEAR-2000)+d)
    # D=0
    delta_t=(-7.658*np.sin(D)+9.863*np.sin(2*D+3.5932))
    return delta_t

def getEoT_TABLE(t):    #[sec] time passed since jan. 1. 0:00
    d=int(t/86400)%365
    return -1*np.array(EOT_TABLE[d])/60

def getEoT_Fourier(t):  #[sec] time passed since jan. 1. 0:00
    t=t-12*86400    # WTF
    JD_2000     = getJulianDate(2000,1,1,0)
    JD_days     = t/86400 - JD_2000
    Cycle = (4 * JD_days) % 1461.
    Theta = Cycle * 0.004301
    EoT1 = 7.353 * np.sin(1 * Theta + 6.209)
    EoT2 = 9.927 * np.sin(2 * Theta + 0.37)
    EoT3 = 0.337 * np.sin(3 * Theta + 0.304)
    EoT4 = 0.232 * np.sin(4 * Theta + 0.715)
    EoT = 0.019 + EoT1 + EoT2 + EoT3 + EoT4
    return -1*EoT

def getEoT_original(Y,M,D,UT):  #[year][month][date] Something fishy    https://articles.adsabs.harvard.edu//full/1989MNRAS.238.1529H/0001529.000.html
    # step A
    # Y=2000
    # M=1
    # D=1
    # UT=12
    if M>2:
        y=Y
        m=M-3
    else:
        y=Y-1
        m=M+9

    J=int(365.25*(y+4712))+(30.6*m+0.5)+59+D-0.5
    G=38-int(3*int(49+y/100)/4)
    JD=J+G  #Julian Date
    print(f"JD= {JD}")  # ez ok
    #step B
    t=(JD+UT/24-2451545.0)/36525
    print(f"t=  {t}")
    if Y>=1650 and Y<=1900:
        dT=0
    else:
        dT=int(-3.36+1.35*(t+2.33)**2)*1e-8
    print(f"dT= {dT}")
    T=t+dT
    print(f"T=  {T}")
    #step C
    ST=100.4606-36000.77005*t+0.000388*t**2-3e-8*t**3   # [deg]
    print(f"ST= {ST}    {ST%360}    ?   {6.69276/24*360}   {18.72561/24*360}")
    #step D
    L=280.46607+36000.76980*T+0.0003025*T**2    # [deg]
    G=357.528+35999.0503*T  # [deg]
    eps=23.4393-0.01300*T-0.0000002*T**2+0.0000005*T**3 # [deg]
    C=(1.9146-0.00484*T-0.000014*T**2)*np.sin(G/180*np.pi)+(0.01999-0.00008*T)*np.sin(2*G/180*np.pi)    # [deg]
    print(f"L=   {L}    G=  {G} eps=    {eps}   C=   {C}")
    Lo=L+C-0.0057   # [deg]
    yi=(np.tan(eps/180*np.pi/2)**2)
    f=180/np.pi
    alph=Lo-yi*f*np.sin(2*Lo/180*np.pi)+0.5*yi**2*f*np.sin(4*Lo/180*np.pi)  # [deg]
    print(f"alpha=  {alph}")
    # step E
    # E=(ST+alph)-(15*UT-180)
    E=(ST+alph)
    if E>10:
        E=E-360
    print(f"E=  {E}")
    return(E)

def getJulianDate(Y,M,D,UT):  #[year][month][date]
    # step A
    # Y=2000
    # M=1
    # D=1
    # UT=12
    if M>2:
        y=Y
        m=M-3
    else:
        y=Y-1
        m=M+9

    J=int(365.25*(y+4712))+(30.6*m+0.5)+59+D-0.5
    G=38-int(3*int(49+y/100)/4)
    JD=J+G  #Julian Date
    print(f"JD= {JD}")  # ez ok
    return JD

def getEoT2_0(t0):  #[sec] time passed since 2000.01.01. 00:00
    JD=getJulianDate(2023,1,1,0)-getJulianDate(2000,1,1,0)
    #step B
    t=(JD+t0/86400)/36525
    print(f"t=  {t}")
    #assumed Y>1900
    dT=int(-3.36+1.35*(t+2.33)**2)*1e-8
    T=t+dT
    #step C
    ST=100.4606-36000.77005*t+0.000388*t**2-3e-8*t**3   # [deg]
    # ST=280.88
    print(f"ST= {ST}")
    #step D
    L=280.46607+36000.76980*T+0.0003025*T**2    # [deg]
    G=357.528+35999.0503*T  # [deg]
    eps=23.4393-0.01300*T-0.0000002*T**2+0.0000005*T**3 # [deg]
    C=(1.9146-0.00484*T-0.000014*T**2)*np.sin(G/180*np.pi)+(0.01999-0.00008*T)*np.sin(2*G/180*np.pi)    # [deg]
    print(f"L=   {L}    G=  {G} eps {eps}   C   {C}")
    Lo=L+C-0.0057   # [deg]
    yi=(np.tan(eps/180*np.pi)**2)/2
    f=180/np.pi
    alph=Lo-yi*f*np.sin(2*Lo/180*np.pi)+0.5*yi**2*f*np.sin(4*Lo/180*np.pi)  # [deg]
    print(f"alpha=  {alph}")
    # step E
    UT=(t0-int(t0/86400)*86400)/3600
    E=(ST+alph)-(15*UT-180)
    if E>10:
        E=E-360
    print(f"E=  {E}")
    return(E)

# def getEqtPos2(Y,M,D): # wikipedia alapján https://en.wikipedia.org/wiki/Position_of_the_Sun
#     # step A
#     if M>2:
#         y=Y
#         m=M-3
#     else:
#         y=Y-1
#         m=M+9

#     J=int(365.25*(y+4712))+(30.6*m+0.5)+59+D-0.5
#     G=38-int(3*int(49+y/100)/4)
#     JD=J+G  #Julian Date
#     n=JD-2451545
#     L=(280.460+(0.9856474*n))%360
#     g=357.528+0.9856003*n
#     lamb=L+1.915*np.sin(g/180*np.pi)+0.020*np.sin(2*g/180*np.pi)
    
#     eps=23.439-0.0000004*n

#     RA=np.arctan2(np.cos(eps/180*np.pi)*np.sin(lamb/180*np.pi),np.cos(lamb/180*np.pi))
#     DEC=np.arcsin(np.sin(eps/180*np.pi)*np.sin(lamb/180*np.pi))
#     # print(f"lamb=   {lamb}")
#     return RA, DEC


def testEoT():
    Y=2023
    D=1
    UT=12
    val=np.zeros(365)
    val2=np.zeros(365)
    val3=np.zeros(365)
    val5=np.zeros(365)

    # print(getEoT2_0(0))
    print(getEoT_original(2023,1,1,12))

    print("-------------")

    # print(getEoT2_0(365*86400))
    # print(getEoT_original(2023,12,29,0))

    for d in range(len(val)):
        val[d]=getEoT2_0(d*86400)
        val2[d]=getEoT_simple(d*86400)
        val3[d]=getEoT_TABLE(d*86400)
        val5[d]=getEoT_Fourier(d*86400)
        # val[M]=getEoT_original(Y,M+1,D,UT)

    plt.plot(val,"-")
    plt.plot(val2,"-")
    plt.plot(val3)
    plt.plot(val5)
    plt.legend(["eot2","eot_simple","table","Fourier"])
    plt.show()

    val4=[]
    for M in range(12):
        val4.append(getEoT_original(Y,M+1,D,UT)/360*24*60)

    plt.plot(val4)
    plt.show()

def getEclipticEoT(t): #[sec] time passed since jan. 1. 0:00
    delta_t=getEoT_TABLE(t)
    # delta_t=getEoT_simple(t)
    # delta_t=getEoT_Fourier(t)
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

        D=6.24004077+0.01720197*(365.25*(YEAR-2000)+Days)
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
    T=[]
    for D in np.arange(0,365):
        t=D*86400+H*60*60
        S=getHoriz_EoT(t,GeoLat)
        # dt=getEoT_simple(t)
        dt=getEoT_Fourier(t)
        # dt=-getEoT_TABLE(t)
        # S=getHoriz(D*86400+H*60*60,GeoLat)
        azmt0,elev0=horiz2AzEl(S)
        azmtA.append(azmt0/np.pi*180)
        elevA.append(elev0/np.pi*180)
        T.append(dt)
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

    azmtB=[]
    elevB=[]
    # for D in [0,91,182,274]:
    for D in [171,355,78,265]:
        S=getHoriz_EoT((D)*86400+H*60*60,GeoLat)
        # S=getHoriz((D)*86400+H*60*60,GeoLat)
        azmt0,elev0=horiz2AzEl(S)
        azmtB.append(azmt0/np.pi*180)
        elevB.append(elev0/np.pi*180)
    plt.plot(azmtB,elevB,'o',color=[0,1,0])

    plt.grid("minor")
    plt.title("Horizontal position of the Sun at Greenwhich every day at 12:00")
    plt.xlabel("Azimuth[˚]")
    plt.ylabel("Altitude[˚]")
    plt.xlim([176,185])
    plt.ylim([0,70])
    plt.savefig("analemma.png")
    plt.show()


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

# csv_read.getEOT_csv()

analemmaCheck()

# testEoT()

# print(getEquatEoT(0))


plt.figure(figsize=(5, 8), dpi=100)


#for analemmas with EoT
Hours=np.arange(12,20)
# Hours=np.array([12])
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
        plt.plot(np.multiply(-1,Vy), Vx, '-', color="black", alpha=0.8)
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