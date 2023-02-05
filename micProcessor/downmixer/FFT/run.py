import matplotlib.pyplot as plt
import numpy as np
import struct


fs=44100
fm=20000

size=int(fs/10)

alp=0.01
DEC=10
BW=100
# BW=int(size/2)


ang=np.arange(size)/fs*2*np.pi*fm
sig=np.exp(1j*ang)


lngt=1	#futószalag hossza
convBelt=np.zeros(size*lngt)+1j*np.zeros(size*lngt)
numLPF=np.zeros(size)+1j*np.zeros(size)

# y=np.arange(size*lngt,0,-1)

fig, ax = plt.subplots()
# (lineR,) = ax.plot(y[::DEC], np.real(convBelt[::DEC]), animated=True)
# (lineI,) = ax.plot(y[::DEC], np.imag(convBelt[::DEC]), animated=True)
# (lineAp,) = ax.plot(y[::DEC], np.abs(convBelt[::DEC]), '--', color='grey', alpha=0.5, animated=True)
# (lineAn,) = ax.plot(y[::DEC], -np.abs(convBelt[::DEC]), '--', color='grey', alpha=0.5, animated=True)
# (fft,) = ax.plot(np.log10(np.real(np.fft.fft(convBelt[::DEC]))), animated=True)
# (fft,) = ax.plot(np.fft.fftshift(np.log10(np.abs(np.fft.fft(numLPF))))[(int(size/2)-200):(int(size/2)+200):], '.-', animated=True)

(fft,) = ax.plot(np.fft.fftshift(20*np.log10(np.abs(np.fft.fft(numLPF))))[(int(size/2)-BW):(int(size/2)+BW):], animated=True)
# (fft,) = ax.plot(np.fft.fftshift(np.abs(np.fft.fft(numLPF))), animated=True)
# (fft,) = ax.plot(np.fft.fftshift(np.abs(np.fft.fft(numLPF))), '.-', animated=True)

plt.show(block=False)
plt.xlabel('minta')
plt.ylabel('érték')
plt.title('Mikrofonminták ábrázolása')
# plt.gca().invert_xaxis()
plt.grid()
plt.xlim([0,2*BW])
plt.ylim([-50, 50])
# plt.ylim([0, 0.01])
plt.pause(0.1)
bg = fig.canvas.copy_from_bbox(fig.bbox)
ax.draw_artist(fft)
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
    # FFT=np.log10(np.abs(np.fft.fft(convBelt[::DEC])))
    FFT=np.fft.fftshift(20*np.log10(np.abs(np.fft.fft(numLPF))))[(int(size/2)-BW):(int(size/2)+BW):]#[(int(size/2)-200):(int(size/2)+200):]
    # FFT=np.fft.fftshift(np.abs(np.fft.fft(numLPF)))[(int(size/2)-BW):(int(size/2)+BW):]

    # FFT=np.fft.fftshift(np.abs(np.fft.fft(numLPF)))#[(int(size/2)-200):(int(size/2)+200):]

    fig.canvas.restore_region(bg)
    fft.set_ydata(FFT)
    ax.draw_artist(fft)
    fig.canvas.blit(fig.bbox)
    fig.canvas.flush_events()