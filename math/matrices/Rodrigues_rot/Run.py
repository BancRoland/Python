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
    # print(f"np.cos(theta) = {np.cos(theta)}")
    # print(f"v= {v}")
    # print(f"np.multiply(np.cos(theta),v)= {np.multiply(np.cos(theta),v)}")
    v_rot=np.multiply(np.cos(theta),v)+np.multiply(np.cross(k,v),np.sin(theta))+np.multiply(np.multiply(k,np.dot(k,v)),(1-np.cos(theta)))
    return v_rot

v=[0,1,0]
print(np.linalg.norm(v))

print(rotX(v,1))
print(rotY(v,1))
print(rotZ(v,1))

print(rotX(np.array([0,1,0]),np.pi/2))
print(rotY(np.array([0,0,1]),np.pi/2))
print(rotZ(np.array([1,0,0]),np.pi/2))

print(ROT(v,np.array([0,0,1]),1))



# # Create a figure and a 3D axis
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')


# Set labels for the axes
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_zlabel('Z-axis')

axis=np.array([1,0,0])
for th in np.arange(0,2*np.pi,0.3):
    w=ROT(v,axis,th)
    ax.scatter(w[0], w[1], w[2])

    ax.set_xlim(-2, 2)  # Set limits for the x-axis
    ax.set_ylim(-2, 2)  # Set limits for the y-axis
    ax.set_zlim(-2, 2)  # Set limits for the z-axis



plt.show()