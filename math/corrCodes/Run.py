import numpy as np
import matplotlib.pyplot as plt
import math

LEN=16
N=128

def WRK(V):
    V=np.array(V)
    W=2*V-np.ones(len(V))
    return W


def WRK_QPSK(V):
    V=np.array(V)
    W=np.exp(1j*V/4*(2*math.pi))
    return(W)

A=[1,1,1,1,1,-1,-1,1,1,-1,1,-1,1]

# B=WRK(np.array([0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1]))
# C=WRK(np.array([0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1]))
# D=WRK(np.array([0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1]))
# E=WRK(np.array([0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1]))

# B=WRK(np.floor(2*np.random.rand(16)))
# C=WRK(np.floor(2*np.random.rand(16)))
# D=WRK(np.floor(2*np.random.rand(16)))
# E=WRK(np.floor(2*np.random.rand(16)))

# Z=np.concatenate([B,C,D,E])


Z40=WRK_QPSK(np.floor(4*np.random.rand(LEN*N)))
Z4=np.concatenate([Z40,np.zeros(1000)])
# Z2=WRK(np.floor(2*np.random.rand(LEN*N)))

IMG=np.zeros([0,3062])
for i in range(N):
    corr=np.correlate(Z4,Z4[LEN*i:LEN*(i+1)-1],'full')
    print(len(corr))
    for j in range(10):
        IMG=np.vstack([IMG,corr])
    # plt.plot(corr,'.')
plt.imshow(np.abs(IMG))
plt.show()

# Z4P=[]
# for i in range(N):
#     Z4P=np.concatenate([np.concatenate([Z4P,np.zeros(1000)]),Z4[LEN*i:LEN*(i+1)-1],np.zeros(1000)])

# plt.step(np.real(Z4P),'.-')
# plt.step(np.imag(Z4P),'.-')
# plt.show()

# out=np.correlate(Z4,Z4P,'full')
# plt.plot(np.real(out),'.-')
# plt.plot(np.imag(out),'.-')
# plt.show()

# W=1999
# IMG=np.zeros([0,W])
# for i in range(30):
#     IMG=np.vstack([IMG,out[i*W:(i+1)*W]])
# plt.imshow(np.abs(IMG))
# plt.show()

# for i in range(N):
#     plt.plot((np.correlate(Z4,Z4[LEN*i:LEN*(i+1)-1],'full')),'.')
# plt.show()