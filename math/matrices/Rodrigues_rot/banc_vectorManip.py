import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def rotX(v_in, theta):
    M = np.array([  [   1,  0,              0               ], 
                    [   0,  np.cos(theta),  -np.sin(theta)  ],
                    [   0,  np.sin(theta),  np.cos(theta)   ]])
    return(M@v_in)

def rotY(v_in, theta):
    M = np.array([  [   np.cos(theta),  0,  np.sin(theta)   ], 
                    [   0,              1,  0               ],
                    [   -np.sin(theta), 0,  np.cos(theta)   ]])
    return(M@v_in)

def rotZ(v_in, theta):
    M = np.array([  [   np.cos(theta),  -np.sin(theta), 0   ], 
                    [   np.sin(theta),  np.cos(theta),  0   ],
                    [   0,              0,              1   ]])
    return(M@v_in)

def ROT(v, ax, theta):
    k=ax/np.linalg.norm(ax)
    v_rot=np.multiply(np.cos(theta),v)+np.multiply(np.cross(k,v),np.sin(theta))+np.multiply(np.multiply(k,np.dot(k,v)),(1-np.cos(theta)))
    return v_rot

def LPitrsect(n,P,v,L): #n: normal vector of plane, P: point of plane, v: direction of line, L: point of line
    t=np.dot(n,(P-L))/np.dot(n,v)
    return(L+np.dot(v,t))

def LayPlane(n,P):   #n: normal vector of the plane,P point on the plane to be laid
    n=n/np.linalg.norm(n)
    z=np.array([0,0,1])
    a=np.cross(n,z)
    th=np.arccos(np.dot(n,z))
    if th >= 0.001:
        out=ROT(P,a,th)
    else:
        out=P
    return out

# v=[0,1,0]
# print(np.linalg.norm(v))

# print(rotX(v,1))
# print(rotY(v,1))
# print(rotZ(v,1))

# print(rotX(np.array([0,1,0]),np.pi/2))
# print(rotY(np.array([0,0,1]),np.pi/2))
# print(rotZ(np.array([1,0,0]),np.pi/2))

# print(ROT(v,np.array([0,0,1]),1))

P=np.array([0,0,2])
n=np.array([5,3,2])
L=np.array([1,2,3])
v=np.array([3,7,9])
print(LPitrsect(n,P,v,L))


# P=np.array([0,0,0])
# n=np.array([0,0,1])
# L=np.array([0,0,1])
# # v=np.array([3,7,9])
# A=np.array([np.cos(23.5/180*np.pi),0,np.sin(23.5/180*np.pi)])
# rotvals=np.arange(0,2*np.pi,0.1)
# plt.plot()
# for i in rotvals:
#     S=rotY(rotZ(A,i),(90-47)/180*np.pi)
#     I=LPitrsect(n,P,S,L)
#     print(I)

#     if np.dot(n,S)>0:
#         plt.scatter(I[0],I[1])
# plt.show()



# # # Create a figure and a 3D axis
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')


# # Set labels for the axes
# ax.set_xlabel('X-axis')
# ax.set_ylabel('Y-axis')
# ax.set_zlabel('Z-axis')

# axis=np.array([1,0,0])
# for th in np.arange(0,2*np.pi,0.3):
#     w=ROT(v,axis,th)
#     ax.scatter(w[0], w[1], w[2])

#     ax.set_xlim(-2, 2)  # Set limits for the x-axis
#     ax.set_ylim(-2, 2)  # Set limits for the y-axis
#     ax.set_zlim(-2, 2)  # Set limits for the z-axis



# plt.show()