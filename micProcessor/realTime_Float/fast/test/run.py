import matplotlib.pyplot as plt
import numpy as np
import struct

def convI32(v):
	num=v[3]+256*v[2]+256**2*v[1]+256**3*v[0]
	return num

def dd(v):
	return(v*2)

size=2**10

fig, axes = plt.subplots()
fig.show()
fig.canvas.draw()
line1 = axes.plot(np.zeros(size))[0]
line2 = axes.plot(np.zeros(size))[0]
#axes.set_ylim(-1, 1)
#background = fig.canvas.copy_from_bbox(axes.bbox)


file = open("pipe", "rb")
byte = file.read(4*size)
while byte:
    byte = file.read(4*size)
    num2=np.array(struct.unpack("<" + "f" * size, byte))

    #fig.canvas.restore_region(background)
    line1.set_ydata(num2)
    line2.set_ydata(num2/2)
    axes.draw_artist(line1)
    axes.draw_artist(line2)
    fig.canvas.blit(axes.bbox)

    """
    plt.ion()
    plt.clf()
    plt.plot(num2)
    plt.ylim([-1, 1])
    plt.show()
    plt.pause(.000001)
    """
