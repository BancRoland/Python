import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

my_dpi=96

size=10
r=0.01*np.random.randn(size, size)
r[5,5]=10
# r=np.zeros([size,size])
# r[0:int(size/3),0:int(size/3)]=1

# for i in range(int(size/5)):
#     for j in range(int(size/5)):
#         r[i,j]=1
# plt.figure(figsize=(size/my_dpi, size/my_dpi), dpi=my_dpi)
plt.imshow(r, cmap="bwr")
plt.show()

Fr=np.fft.fft2(r)

plt.imshow(np.abs(Fr), cmap="gray")
plt.show()

plt.imshow(np.fft.fftshift(np.abs(Fr)), cmap="gray")
plt.show()

n=10
# # R=np.zeros([size*n,size*n])
# R=np.concatenate([Fr,np.zeros([size,size])],axis=0)
# R=np.concatenate([R,np.zeros([2*size,size])],axis=1)

R=np.concatenate([Fr[0:int(size/2),:],np.zeros([(n-1)*size,size]),Fr[-int(size/2):,:]],axis=0)
# R=np.concatenate([Fr[0:int(size/2)],np.zeros([size,size]),Fr[-int(size/2):]],axis=0)
R=np.concatenate([R[:,0:int(size/2)],np.zeros([size*n,(n-1)*size]),R[:,-int(size/2):]],axis=1)

# R[0:int(size/2),0:int(size/2)]=Fr[0:int(size/2),0:int(size/2)]
# R[-int(size/2):,-int(size/2):]=Fr[-int(size/2):,-int(size/2):]
# R[-int(size/2):,0:int(size/2)]=Fr[-int(size/2):,0:int(size/2)]
plt.imshow(np.abs(R), cmap="gray")
plt.show()

plt.subplot(3,1,1)
plt.imshow(r, cmap="bwr")
plt.subplot(3,1,2)
plt.imshow(np.real(np.fft.ifft2(R)), cmap="bwr")
for i in n*np.arange(size):
    for j in n*np.arange(size):
        plt.scatter(i,j,color="black", alpha=0.2)
plt.subplot(3,1,3)
plt.imshow(np.imag(np.fft.ifft2(R)), cmap="bwr")
for i in n*np.arange(size):
    for j in n*np.arange(size):
        plt.scatter(i,j,color="black", alpha=0.2)
plt.show()




fig = plt.figure(figsize =(14, 9))
ax = plt.axes(projection ='3d')
 
# Creating plot
x = np.outer(np.arange(np.shape(R)[0]), np.shape(R)[0])
y = x.copy().T # transpose
ax.plot_surface(x,y,np.real(np.fft.ifft2(R)),cmap='viridis', edgecolor='none')
ax.grid(False)
plt.show()