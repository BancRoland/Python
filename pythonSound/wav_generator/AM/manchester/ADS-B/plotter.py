import matplotlib.pyplot as plt
import numpy as np
import struct
import argparse

print("usage: python3 plotter.py [-s/size 3] [-l/lngt 30] [-A/Amp 0.5]")

parser = argparse.ArgumentParser(description="set the displey options:\n[size=3]: (2^(?) sample long chunk)\n[lngt=30]: number of chuncks displayed\n[Amp=0.5] amplitude of display\n python3 plotter.py 3 30 0.5")

parser.add_argument("-s","--size", help="2^(?) sample long chunk", nargs='?', type=int, const=1, default=3)
parser.add_argument("-l","--lngt", help="number of chuncks displayed", nargs='?', type=int, const=1, default=30)
parser.add_argument("-A","--Amp", help="amplitude of display", nargs='?', type=float, const=1, default=0.5)

args=parser.parse_args()

if (args.size == None):
        parser.print_help()


size=2**args.size
lngt=args.lngt	#futószalag hossza
Amp=args.Amp


convBelt=np.exp(1j*np.zeros(size*lngt))
y=np.arange(size*lngt,0,-1)

fig, ax = plt.subplots()
#(lineR,) = ax.plot(y, np.real(convBelt), '.-', animated=True)
#(lineI,) = ax.plot(y, np.imag(convBelt), '.-', animated=True)
(lineR,) = ax.plot(y, np.real(convBelt), animated=True)
(lineI,) = ax.plot(y, np.imag(convBelt), animated=True)
(lineAp,) = ax.plot(y, np.abs(convBelt), '--', color='grey', alpha=0.5, animated=True)
(lineAn,) = ax.plot(y, -1*np.abs(convBelt), '--', color='grey', alpha=0.5, animated=True)

plt.show(block=False)
plt.xlabel('minta')
plt.ylabel('érték')
plt.title('Mikrofonminták ábrázolása')
plt.gca().invert_xaxis()
plt.grid()
plt.ylim([-Amp, Amp])
plt.pause(0.1)
bg = fig.canvas.copy_from_bbox(fig.bbox)
ax.draw_artist(lineR)
ax.draw_artist(lineI)
ax.draw_artist(lineAp)
ax.draw_artist(lineAn)


fig.canvas.blit(fig.bbox)


file = open("pipe", "rb")
byte = file.read(4*size)
while byte:
    byte = file.read(4*size*2)
    num2=np.array(struct.unpack("<" + "f" * size*2, byte))
    num3=num2[0::2]+1j*num2[1::2]
    convBelt[0:-size]=convBelt[size:]
    convBelt[-size:]=num3

    fig.canvas.restore_region(bg)
    lineI.set_ydata(np.imag(convBelt))
    lineR.set_ydata(np.real(convBelt))
    lineAp.set_ydata(np.abs(convBelt))
    lineAn.set_ydata(-1*np.abs(convBelt))
    ax.draw_artist(lineR)
    ax.draw_artist(lineI)
    ax.draw_artist(lineAp)
    ax.draw_artist(lineAn)
    fig.canvas.blit(fig.bbox)
    fig.canvas.flush_events()
 
