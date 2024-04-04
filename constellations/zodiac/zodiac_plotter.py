import matplotlib.pyplot as plt
import numpy as np
from numpy import sin, cos, pi

def upproject(v):
    v=+np.array(v)+np.array([0,0,1])
    w=v/v[2]
    return w

def cylinder_project(v):
    x = np.arctan2(v[0],v[1])
    # y=v[2]
    y=np.arcsin(v[2])
    w = np.array([x,y])
    return w

def xrot(v,alpha_deg):
    alp=alpha_deg/180*pi
    R=np.array([[1,0,0],[0,cos(alp),-sin(alp)],[0,sin(alp),cos(alp)]])
    return v @ R

const=np.load("stars_test.npy", allow_pickle=True)
# const=np.load("stars.npy", allow_pickle=True)
a=1.5
hmg=4
hmg2=2


# for star in const:
#     if star["Apparent Magnitude"] <= hmg:
#         ra  = star['Right Ascension (deg)']/180*pi
#         dec = star['Declination (deg)']/180*np.pi
#         v=[cos(ra)*cos(dec),sin(ra)*cos(dec), sin(dec)]
#         plt.scatter(v[1], v[0], color="black",  s=a*(1+hmg-star['Apparent Magnitude']))
# plt.grid()
# plt.gca().set_aspect('equal', adjustable='box')
# plt.show()

plt.figure(figsize=(12, 8)) 
for star in const:
    ra  = star['Right Ascension (deg)']/180*pi
    dec = star['Declination (deg)']/180*np.pi
    v = np.array([cos(ra)*cos(dec),sin(ra)*cos(dec), sin(dec)])
    v = xrot(v,23.5)
    w = upproject(v)
    if star['Apparent Magnitude'] <= hmg:
        S=star['Apparent Magnitude']
        alpha=1
    else:
        S=hmg
        alpha=0.5
    if star['Apparent Magnitude'] <= hmg2:
        marker='*'
    else:
        marker='.'
    plt.scatter(w[1], w[0], color="black",  s=a*(1+hmg-S), marker=marker, alpha=alpha)
# plt.grid()
plt.gca().set_aspect('equal', adjustable='box')
plt.savefig("toprinit.png")
plt.show()

plt.figure(figsize=(12, 8)) 
for star in const:
    ra  = star['Right Ascension (deg)']/180*pi
    dec = star['Declination (deg)']/180*np.pi
    v = np.array([cos(ra)*cos(dec),sin(ra)*cos(dec), sin(dec)])
    v = xrot(v,23.5)
    w = cylinder_project(v)
    if star['Apparent Magnitude'] <= hmg:
        S=star['Apparent Magnitude']
        alpha=1
    else:
        S=hmg
        alpha=0.5
    if star['Apparent Magnitude'] <= hmg2:
        marker='*'
    else:
        marker='.'
    plt.scatter(w[0], w[1], color="black",  s=a*(1+hmg-S), marker=marker, alpha=alpha)
plt.xlabel('Right Ascension (deg)') 
plt.ylabel('Declination (deg)')
plt.xlim([-np.pi,np.pi])
# plt.ylim([-1,1])
plt.ylim([-np.pi/2,np.pi/2])
# plt.grid()
# plt.axhline(0, color="gray",alpha=0.3)
# plt.axvline(180, color="gray",alpha=0.3)
# plt.gca().invert_xaxis()
plt.gca().set_aspect('equal', adjustable='box')
plt.savefig("toprinit2.png")
plt.show()