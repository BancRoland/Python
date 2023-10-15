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
    # ecV=eclipticCoord(t)
    # eqV=eclip2eqat(ecV)
    eqV=getEquat(t)
    eqV2=equatRot(t,eqV)
    horiz=equat2horiz(eqV2,GeoLat)
    return horiz

def horizOfDate(D,GeoLat,H):
    S=vMp.rotZ(np.array([1,0,0]),D*2*np.pi)
    S=vMp.rotX(S,23.5/180*np.pi)
    S=vMp.rotZ(S,-((D+H/D_sol)*2*np.pi))
    S=vMp.rotY(S,(90-GeoLat)/180*np.pi) #X irányba van észak
    # ecV=eclipticCoord(D*86400)
    # eqV=eclip2eqat(ecV)
    # eqV2=equatRot((D+H/D_sol)*86400,eqV)
    # horiz=equat2horiz(eqV2,GeoLat)
    return S

def middleSun(D):
    return vMp.rotZ(np.array([1,0,0]),D*2*np.pi)


def getEquat(t):
    ecV=eclipticCoord(t)
    eqV=eclip2eqat(ecV)
    return eqV

def getEquatEoT2(t):
    v=getEquat(t)
    v=vMp.LPitrsect(z,O,z,v)
    v=vMp.norm(v)
    v=vMp.rotZ(v,0.1)
    v=vMp.LPitrsect(RotAx,O,z,v)
    v=vMp.norm(v)
    return v
    

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


def TimeEqZ():
    delta_t=[]
    harm1=[]
    harm2=[]
    Days=np.arange(0,365)
    for d in Days:
        D=6.24004077+0.01720197*(365.25*(YEAR-2000)+d+FindZero())
        delta_t.append(-7.658*np.sin(D)+9.863*np.sin(2*D+3.5932))
    #     harm1.append(-7.658*np.sin(D))
    #     harm2.append(9.863*np.sin(2*D+3.5932))
    # harm1=np.array(harm1)*60/86400*2*np.pi
    # harm2=np.array(harm2)*60/86400*2*np.pi
    # plt.plot(harm1)
    # plt.plot(harm2)
    # plt.plot(np.array(harm1)+np.array(harm2))
    plt.plot(delta_t)
    plt.grid()
    plt.xlabel("time since spring eq [days]")
    plt.ylabel("diff in Retascence [deg]")
    plt.title("Difference in rectascence between actual sun and fictive equatorial middlesun")
    plt.show()

def getEquatEoT(t):
    # delta_t=[]
    # harm1=[]
    # harm2=[]
    d=t/86400
    D=6.24004077+0.01720197*(365.25*(YEAR-2000)+d+FindZero())
    # D=6.24004077+0.01720197*(365.25*(YEAR-2000)+d)
    delta_t=(-7.658*np.sin(D)+9.863*np.sin(2*D+3.5932))
    # delta_t=5
    #     harm1.append(-7.658*np.sin(D))
    #     harm2.append(9.863*np.sin(2*D+3.5932))
    # harm1=np.array(harm1)*60/86400*2*np.pi
    # harm2=np.array(harm2)*60/86400*2*np.pi
    delta_t=np.array(delta_t)/60/24*np.pi*2
    # print(delta_t)
    # delta_t=0.1

    v=getEquat(t)
    v=vMp.LPitrsect(z,O,z,v)
    v=vMp.norm(v)
    v=vMp.rotZ(v,-delta_t)
    v=vMp.LPitrsect(RotAx,O,z,v)
    v=vMp.norm(v)

    return v

    # v=vMp.rotZ(x,(d+delta_t)/365.25*2*np.pi)

    # I=vMp.LPitrsect(RotAx,O,z,v)
    # # print(I)
    # # print(np.array(I)
    # if np.linalg.norm(I) >= 1e-10:
    #     # I=I/np.linalg.norm(I)
    #     I=vMp.norm(I)
    # else:
    #     I=np.array([0,0,0])
    # return I


def getHoriz_EoT(t,GeoLat):
    # ecV=eclipticCoord(t)
    # eqV=eclip2eqat(ecV)
    eqV=getEquatEoT(t)
    eqV2=equatRot(t,eqV)
    horiz=equat2horiz(eqV2,GeoLat)
    return horiz

def wtf_equat():
    normal_x=[]
    normal_y=[]
    normal_z=[]
    eot_x=[]
    eot_y=[]
    eot_z=[]

    for d in np.arange(0,365):
        t=d*86400

        eqV=getEquat(t)
        n=vMp.rotZ(eqV,0)
        n=vMp.rotZ(eqV,(t/-(D_sid*60*60)*2*np.pi))

        eqV=getEquatEoT(t)
        e=vMp.rotZ(eqV,0)
        e=vMp.rotZ(eqV,(t/-(D_sid*60*60)*2*np.pi))


        normal_x.append(n[0])
        normal_y.append(n[1])
        normal_z.append(n[2])

        eot_x.append(e[0])
        eot_y.append(e[1])
        eot_z.append(e[2])

    normal_x=np.array(normal_x)
    normal_y=np.array(normal_y)
    normal_z=np.array(normal_z)
    eot_x=np.array(eot_x)
    eot_y=np.array(eot_y)
    eot_z=np.array(eot_z)
    plt.plot(normal_x,".",color="C0")
    plt.plot(normal_y,".",color="C1")
    plt.plot(normal_z,".",color="C2")

    plt.plot(eot_x,color="C0",linestyle="-")
    plt.plot(eot_y,color="C1",linestyle="-")
    plt.plot(eot_z,color="C2",linestyle="-")

    plt.grid()

    plt.legend(["x","y","z"])
    plt.show()



def TimeEq2():
    B=[]
    C=[]
    for D in np.arange(0,366):
        b=np.arctan2(getEquat(D*86400)[1],getEquat(D*86400)[0])
        c=np.arctan2(middleSun(D/365.25)[1],middleSun(D/365.25)[0])
        B.append(b)
        C.append(c)
    E=np.array(C)-np.array(B)
    plt.plot(E/2/np.pi*60*24)
    plt.grid()
    plt.xlabel("time since spring eq [days]")
    plt.ylabel("diff in Retascence [deg]")
    plt.title("Difference in rectascence between actual sun and fictive equatorial middlesun")
    plt.show()


def TimeEq_EoT():
    B=[]
    C=[]
    F=[]
    G=[]
    EoT_x=[]
    EoT_y=[]
    EoT_z=[]
    MS_x=[]
    MS_y=[]
    MS_z=[]
    delta_t=[]
    for Days in np.arange(0,366):
        EoT=getEquatEoT(Days*86400)
        # EoT=getEquat(Days*86400)
        EoT[2]=0
        EoT_x.append(EoT[0])
        EoT_y.append(EoT[1])
        EoT_z.append(EoT[2])
        MS=middleSun(Days/365.25)
        MS_x.append(MS[0])
        MS_y.append(MS[1])
        MS_z.append(MS[2])
     
        g=vMp.XY_plane_angleDiff(MS,EoT)/2/np.pi*365.25*24*60

        # b=np.arctan2(getEquatEoT(Days*86400)[1],getEquatEoT(Days*86400)[0])
        # f=np.arctan2(getEquat(Days*86400)[1],getEquat(Days*86400)[0])
        # c=np.arctan2(middleSun(Days/365.25)[1],middleSun(Days/365.25)[0])

        D=6.24004077+0.01720197*(365.25*(YEAR-2000)+Days+FindZero())
        delta_t.append(-7.658*np.sin(D)+9.863*np.sin(2*D+3.5932))

        # B.append(b)
        # C.append(c)
        # F.append(f)
        G.append(g)
    B=np.array(B)
    C=np.array(C)
    E=np.array(C)-np.array(B)
    F=np.array(C)-np.array(F)

    # plt.plot(B/2/np.pi*365.25)
    # plt.plot(C/2/np.pi*365.25)
    # plt.plot(E/2/np.pi*24*60)
    # plt.plot(F/2/np.pi*24*60)
    # plt.plot(G)
    plt.plot(MS_x,color="C0")
    plt.plot(MS_y,color="C1")
    plt.plot(MS_z,color="C2")
    plt.grid()
    plt.xlabel("time since spring eq [days]")
    plt.ylabel("diff in Retascence [deg]")
    plt.title("MS")

    plt.plot(EoT_x,color="C0",linestyle=":")
    plt.plot(EoT_y,color="C1",linestyle=":")
    plt.plot(EoT_z,color="C2",linestyle=":")
    plt.grid()
    plt.xlabel("time since spring eq [days]")
    plt.ylabel("diff in Retascence [deg]")
    plt.title("EoT")
    plt.show()

    plt.plot(G)
    plt.show()




HourDiff=GeoLon/360*24-GMT
print(HourDiff)



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

# TimeEq2()

# TimeEqZ()

# TimeEq_EoT()


# wtf_equat()

########
# print(f"eqinox is day :{FindZero()}")

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
        # S3=getHoriz(D*86400+H*60*60,GeoLat)
        S3=getHoriz_EoT(D*86400+H*60*60,GeoLat)
        

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


# for single point
H=12
D=0
H=H+HourDiff
# S=getHoriz(D*86400+H*60*60,GeoLat)
# S=horizOfDate(D, GeoLat, H)
S=getHoriz_EoT(D*86400+H*60*60,GeoLat)
I=vMp.LPitrsect(n,P,S,L)
I=vMp.rotZ(I,azmt-np.pi/2)
I=vMp.rotY(I,np.pi/2)
if np.dot(n,S)>0:
    plt.scatter(np.multiply(-1,I[1]), I[0], color="red", alpha=0.8, marker="o")

#for dotted lines of extremes
# Hours=np.arange(8,16,0.1)
# Dates=np.multiply(365.2422,np.array([0,1/4,2/4,3/4]))
Hours=np.arange(0,24,0.1)
Dates=np.array([0,1/4,2/4,3/4])
for D in Dates:
    Vx=[]
    Vy=[]
    Vz=[]
    for H in Hours:
        H=H+HourDiff
        S=horizOfDate(D, GeoLat, H)
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

Hours=np.arange(12,15)
Hours=np.array([0,2,3,5,6,7])
Hours=np.array([12,13,15,16,17])
Hours_Labels=["XII0","I0","II0","III0","IIII0","V0","VI0","VII0","VIII0","IX","X","XI","XII","I","II","III","IIII","V","VI","VII","VIII","IX","X","XI"]
Dates=np.array([1/4])*366
for D in Dates:
    Vx=[]
    Vy=[]
    for h in Hours:
        H=h+HourDiff
        # S=horizOfDate(D, GeoLat, H)
        # S=getHoriz_EoT(D*86400+H*60*60,GeoLat)
        S=getHoriz(D*86400+H*60*60,GeoLat)
        I=vMp.LPitrsect(n,P,S,L)
        I=vMp.rotZ(I,azmt-np.pi/2)
        I=vMp.rotY(I,np.pi/2)
        
        I=polarIntersect+1.1*(I-polarIntersect)
        I_N=polarIntersect+1.05*(I-polarIntersect)

        
        if np.dot(n,S)>0:
            plt.text(-1*I_N[1], I_N[0], Hours_Labels[h], horizontalalignment='center', verticalalignment='center', size=12, weight="bold", font="serif")
                    
            Vx=np.zeros(2)
            Vx[0]=I[0]
            Vx[1]=polarIntersect[0]

            Vy=np.zeros(2)
            Vy[0]=I[1]
            Vy[1]=polarIntersect[1]
            plt.plot(np.multiply(-1,Vy), np.multiply(1,Vx), color="black", alpha=0.5, linestyle=':')



# I=polarIntersect+1.1*(I-polarIntersect)
# I_N=polarIntersect+1.05*(I-polarIntersect)

# if np.dot(n,S)>0:
#     # plt.text(-1*I_N[1], I_N[0], Hours_Labels[Hours[h]], horizontalalignment='center', verticalalignment='center', size=12, weight="bold", font="serif")
#     plt.scatter(np.multiply(-1,I[1]), I[0], color="green", alpha=0.8, marker="o") 
#     Vx=np.zeros(2)
    # Vx[0]=I[0]
    # Vx[1]=polarIntersect[0]

    # Vy=np.zeros(2)
    # Vy[0]=I[1]
    # Vy[1]=polarIntersect[1]
    # plt.plot(np.multiply(-1,Vy), np.multiply(1,Vx), color="black", alpha=0.5, linestyle=':')




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