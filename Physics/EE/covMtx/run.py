import matplotlib.pyplot as plt
import numpy as np

def sind(alpha):
    return np.sin(alpha/180*np.pi)

def phases(dir,N,lmbda,D,startphase):
    p = sind(dir)*D*np.arange(N)/lmbda*2*np.pi
    v = np.exp(1j*(p+startphase))*np.ones([1,N])
    return v

def herm(v):
    return np.conjugate(np.transpose(v))

N = 20    # [] number of antenna elements
dir1 = -11  # [deg] doa
dir2 = -20  # [deg] doa
A1 = 1
A2 = 1
lmbda = 2    # [m] wavelength
D = 1         # [m] distance of elements

# p = sind(dir)*D*np.arange(N)/lmbda*2*np.pi
# v = np.exp(1j*p)
v = A1*phases(dir1,N,lmbda,D,0)+A2*phases(dir2,N,lmbda,D,0)

if 0:
    plt.plot(np.real(v))
    plt.plot(np.imag(v))
    plt.plot(np.abs(v),linestyle="--",color="gray",alpha=0.5)
    plt.grid()
    plt.show()

pspec = np.fft.fft(v)
angles = np.arange(N)/N*180

if 0:
    plt.plot(angles,np.fft.fftshift(np.abs(pspec)))
    # plt.plot(angles,20*np.log10(np.fft.fftshift(np.abs(pspec))))
    plt.grid()
    plt.xlim([0,180])
    plt.show()

testdeg=np.arange(-90,90,0.01)
out = 1j*np.zeros(len(testdeg))
for i,deg in enumerate(testdeg):
    # out[i] = np.sum(v*np.conj(phases(deg,N,lmbda,D,0)))
    a = phases(deg,N,lmbda,D,0)
    out[i] = v @ herm(a)
if 1:
    plt.plot(testdeg,np.abs(out))
    plt.axvline(dir1)
    plt.axvline(dir2)
    plt.grid()
    plt.show()



# cov = np.outer(v,np.conjugate(v))
cov = 1j*np.zeros([N,N])
for i in range(10000):
    v = A1*phases(dir1,N,lmbda,D,np.random.rand()*np.pi*2) + A2*phases(dir2,N,lmbda,D,np.random.rand()*np.pi*2)
    cov += herm(v) @ v
print(np.linalg.det(cov))
# cov += 1e-6*np.eye(np.shape(cov)[0])
print(np.linalg.det(cov))
print(np.shape(cov))

v=A1*phases(dir1,N,lmbda,D,np.random.rand()*np.pi*2)
cov = herm(v) @ v
v=A2*phases(dir2,N,lmbda,D,np.random.rand()*np.pi*2)
cov = cov + herm(v) @ v
cov += 1e-6*np.eye(np.shape(cov)[0])

eigenvalues, eigenvectors = np.linalg.eig(cov)
max_eig_index = np.argmax(np.abs(eigenvalues))
vmax = eigenvectors[:, max_eig_index]
# print(eigenvalues)
# print(eigenvectors)

if 0:
    plt.plot(np.real(eigenvalues),"o-")
    plt.plot(np.imag(eigenvalues),"o-")
    plt.plot(np.abs(eigenvalues),"o-")
    plt.show()

    plt.subplot(2,1,1)
    plt.plot(np.real(vmax))
    plt.plot(np.imag(vmax))
    plt.plot(np.abs(vmax))
    plt.subplot(2,1,2)
    plt.plot(np.real(v))
    plt.plot(np.imag(v))
    plt.plot(np.abs(v))
    plt.show()

    plt.subplot(1,3,1)
    plt.imshow(np.real(eigenvectors))
    plt.subplot(1,3,2)
    plt.imshow(np.imag(eigenvectors))
    plt.subplot(1,3,3)
    plt.imshow(np.abs(eigenvectors))
    plt.show()


    plt.subplot(1,3,1)
    plt.imshow(np.real(cov))
    plt.subplot(1,3,2)
    plt.imshow(np.imag(cov))
    plt.subplot(1,3,3)
    plt.imshow(np.abs(cov))
    plt.show()

# CAPON

a0 = phases(dir2,N,lmbda,D,0)
w = a0@np.linalg.inv(cov)/(a0@np.linalg.inv(cov)@np.conjugate(np.transpose(a0)))
print(np.shape(a0))
# print(a0@np.linalg.inv(cov)@(np.conjugate(np.transpose(a0))))
# print(np.shape(cov))
# print(np.shape(a))
# print(np.shape(a@cov))
# print(w)

# print(np.linalg.inv(cov)@a)

# v = A1*phases(dir1,N,lmbda,D,0) + A2*phases(dir2,N,lmbda,D,0)
# v = A1*phases(dir1,N,lmbda,D,np.random.rand()*np.pi*2) + A2*phases(dir2,N,lmbda,D,np.random.rand()*np.pi*2)
# cov = herm(v) @ v

testdeg=np.arange(-90,90,0.01)
out = 1j*np.zeros(len(testdeg))

for i,deg in enumerate(testdeg):
    # out[i] = np.sum(w*np.conj(phases(deg,N,lmbda,D,0)))
    a = phases(deg,N,lmbda,D,0)
    # print(np.shape(a))
    out[i] = a @ cov @ herm(a)
    # out[i] = v@herm(a)
if 1:
    plt.plot(testdeg,np.abs(out))
    plt.axvline(dir1)
    plt.axvline(dir2)
    # plt.axhline(1)
    plt.grid()
    plt.show()


testdeg = np.arange(-90,90,0.01)
out = 1j*np.zeros(len(testdeg))

for i,deg in enumerate(testdeg):
    out[i] = np.sum(w*np.conj(phases(deg,N,lmbda,D,0)))
    # a = phases(deg,N,lmbda,D,0)
    # print(np.shape(a))
    # out[i] = w @ cov @ herm(w)
    # out[i] = v@herm(a)
if 1:
    plt.plot(testdeg,np.log10(np.abs(out)))
    plt.axvline(dir1)
    plt.axvline(dir2)
    # plt.axhline(1)
    plt.grid()
    plt.show()