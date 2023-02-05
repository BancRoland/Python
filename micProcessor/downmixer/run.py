import matplotlib.pyplot as plt
import numpy as np
import struct

# def convI32(v):
# 	num=v[3]+256*v[2]+256**2*v[1]+256**3*v[0]
# 	return num

# def dd(v):
# 	return(v*2)

fs=44100
fm=20000

size=int(fs/10)

alp=0.01
DEC=10


ang=np.arange(size)/fs*2*np.pi*fm
sig=np.exp(1j*ang)
# plt.plot(np.real(sig))
# plt.plot(np.imag(sig))
# plt.show()


lngt=10	#futószalag hossza
convBelt=np.zeros(size*lngt)+1j*np.zeros(size*lngt)
numLPF=np.zeros(size)+1j*np.zeros(size)

y=np.arange(size*lngt,0,-1)

fig, ax = plt.subplots()
(lineR,) = ax.plot(y[::DEC], np.real(convBelt[::DEC]), animated=True)
(lineI,) = ax.plot(y[::DEC], np.imag(convBelt[::DEC]), animated=True)
(lineAp,) = ax.plot(y[::DEC], np.abs(convBelt[::DEC]), '--', color='grey', alpha=0.5, animated=True)
(lineAn,) = ax.plot(y[::DEC], -np.abs(convBelt[::DEC]), '--', color='grey', alpha=0.5, animated=True)

plt.show(block=False)
plt.xlabel('minta')
plt.ylabel('érték')
plt.title('Mikrofonminták ábrázolása')
plt.gca().invert_xaxis()
plt.grid()
plt.ylim([-0.1, 0.1])
plt.pause(0.01)
bg = fig.canvas.copy_from_bbox(fig.bbox)
ax.draw_artist(lineR)
ax.draw_artist(lineI)
fig.canvas.blit(fig.bbox)


file = open("pipe", "rb")
byte = file.read(4*size)
while byte:
    byte = file.read(4*size)
    num2=np.array(struct.unpack("<" + "f" * size, byte))
    num3=num2*sig
    numLPF[0]=convBelt[-1]*(1-alp)+num3[0]*alp
    for i in range(size-1):
        numLPF[i+1]=numLPF[i]*(1-alp)+num3[i]*alp

    convBelt[0:-size]=convBelt[size:]
    convBelt[-size:]=numLPF

    fig.canvas.restore_region(bg)
    lineR.set_ydata(np.real(convBelt[::DEC]))
    lineI.set_ydata(np.imag(convBelt[::DEC]))
    lineAp.set_ydata(np.abs(convBelt[::DEC]))
    lineAn.set_ydata(-np.abs(convBelt[::DEC]))
    ax.draw_artist(lineR)
    ax.draw_artist(lineI)
    ax.draw_artist(lineAp)
    ax.draw_artist(lineAn)
    fig.canvas.blit(fig.bbox)
    fig.canvas.flush_events()

 
