import matplotlib.pyplot as plt
import numpy as np
from numpy import sin, cos, pi

def upproject(v):
    v=+np.array(v)+np.array([0,0,1])
    w=v/v[2]
    return w

def xrot(v,alpha_deg):
    alp=alpha_deg/180*pi
    R=np.array([[1,0,0],[0,cos(alp),-sin(alp)],[0,sin(alp),cos(alp)]])
    return v @ R

# const=np.load("stars_test.npy", allow_pickle=True)
const=np.load("stars.npy", allow_pickle=True)
hmg=15
a=0.5

# for star in const:
#     if star["Apparent Magnitude"] <= hmg:
#         # print(star['Name'])
#         plt.scatter(star['Right Ascension (deg)'], star['Declination (deg)'], color="black",  s=a*(1+hmg-star['Apparent Magnitude']))
#         plt.xlabel('Right Ascension (deg)')
#         plt.ylabel('Declination (deg)')
# plt.xlim([0,360])
# plt.ylim([-90,90])
# plt.grid()
# plt.axhline(0, color="gray",alpha=0.3)
# plt.axvline(180, color="gray",alpha=0.3)
# plt.gca().invert_xaxis()
# plt.gca().set_aspect('equal', adjustable='box')
# plt.show()

# for star in const:
#     if star["Apparent Magnitude"] <= hmg:
#         ra  = star['Right Ascension (deg)']/180*pi
#         dec = star['Declination (deg)']/180*np.pi
#         v=[cos(ra)*cos(dec),sin(ra)*cos(dec), sin(dec)]
#         plt.scatter(v[1], v[0], color="black",  s=a*(1+hmg-star['Apparent Magnitude']))
# plt.grid()
# plt.gca().set_aspect('equal', adjustable='box')
# plt.show()

for star in const:
    if star["Apparent Magnitude"] <= hmg:
        ra  = star['Right Ascension (deg)']/180*pi
        dec = star['Declination (deg)']/180*np.pi
        v = np.array([cos(ra)*cos(dec),sin(ra)*cos(dec), sin(dec)])
        v=xrot(v,23.5)
        w = upproject(v)
        plt.scatter(w[1], w[0], color="black",  s=a*(1+hmg-star['Apparent Magnitude']))
plt.grid()
plt.gca().set_aspect('equal', adjustable='box')
plt.show()
