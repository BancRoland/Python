from turtle import color
import matplotlib.pyplot as plt
import csv
import numpy as np
# import pyapril.targetParamCalculator as tpc

# print(dir(pyapril))


cName=[]
cAlt=[]
cVel=[]
cLat=[]
cLon=[]
cAddr=[]

bLat=47.4707
bLon=19.0855

# center_coord = (bLat, bLon, 1110)
# xyz = tpc.lla2enu([34.681,-86.530,1100], center=center_coord)
# print(xyz)

PI=3.1415926535

# out.csv contains all the data neededin the following order:
# [Addres]      [Altitude]  [Speed] [Lat]       [Lon]       [FlightID]
# working example:
# 4901505   	495     	311  	47.4889 	19.1556 	NSZ3550 
# 4901505   	495     	311  	47.4887 	19.1560 	NSZ3550 
# 66023     	2391    	537  	47.4603 	19.4154 	MSR751  
# 4901505   	487     	309  	47.4878 	19.1575 	NSZ3550
#  
with open('out.csv', newline='') as f:
    reader = csv.reader(f, delimiter='	')
    for row in reader:
        cAddr.append(eval(row[0]))
        cAlt.append(eval(row[1]))
        cVel.append(eval(row[2]))
        cLat.append(eval(row[3]))
        cLon.append(eval(row[4]))
        cName.append(row[0])

process_csv_messages(sys.stdin)

# plt.plot(cLat, cLon, '.')
# plt.plot(bLat, bLon, '.')
# plt.legend(["planes","base"])
# plt.grid()
# plt.show()

# # for test purposes:
# cLat=[47, 47, 47, 48, 48, 48]
# cLon=[18, 19, 20, 18, 19, 20]


# According to the spherical coordinate system
a=90*np.ones(len(cLat))-cLat
b=(90-bLat)*np.ones(len(cLat))
gamma=cLon-bLon*np.ones(len(cLon))
c=np.arccos(np.cos(a/180*PI)*np.cos(b/180*PI)+np.sin(a/180*PI)*np.sin(b/180*PI)*np.cos(gamma/180*PI))
R=6371
Ds=R*c

# According to Descart coordinates
dLat=cLat-bLat*np.ones(len(cLat))
dLon=np.cos(bLat/180*PI)*(cLon-bLon*np.ones(len(cLon)))
Dd=40030/360*np.sqrt(dLon**2+dLat**2)

# print(Ds)
# print(Dd)


# print(d0)
# plt.plot(d0,cAlt,'.')
# plt.show()

# print((np.cos(bLat/180*PI)*dLon))
# print((np.arctan2((np.cos(bLat/180*PI)*dLon,dLat))/PI*180)%360)
# print((np.arctan2(np.cos(bLat/180*PI)*dLon,dLat)/PI*180)%360)
azmt=(np.arctan2(dLon,dLat)/PI*180)%360
# print(azmt)

plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.plot(cLon,cLat,'o')
plt.plot(bLon,bLat,'o')
plt.grid(True)

plt.subplot(1, 2, 2, projection='polar')
plt.plot(-azmt/180*PI+PI/2, Dd, 'o')
plt.plot(0,0,'o')
# plt.ylim(0, 50)
plt.grid(True)
plt.show()

radProj=np.sqrt(Dd**2+(np.array(cAlt)/1000)**2)

plt.polar(-azmt/180*PI+PI/2, Dd, 'o', color="gray")
plt.polar(-azmt/180*PI+PI/2, radProj, 'o')
plt.grid(True)
plt.legend(["GeoPosition", "Actual distance"])
plt.show()
# plt.title(f"2023.03.02.\nműholdkeresés parabolával")
# plt.xlabel("azimut [°]")
# plt.ylabel("eleváció [°]")

# plt.grid()
# plt.savefig('data.png', dpi=300, bbox_inches='tight')
# plt.show()
