import matplotlib.pyplot as plt
import numpy as np
import struct

# def convI32(v):
# 	num=v[3]+256*v[2]+256**2*v[1]+256**3*v[0]
# 	return num

# def dd(v):
# 	return(v*2)

size=2**10
lngt=10	#futószalag hossza
convBelt=np.zeros(size*lngt)
y=np.arange(size*lngt,0,-1)

fig, ax = plt.subplots()
(line,) = ax.plot(y, convBelt, animated=True)

plt.show(block=False)
plt.xlabel('minta')
plt.ylabel('érték')
plt.title('Mikrofonminták ábrázolása')
plt.gca().invert_xaxis()
plt.grid()
plt.ylim([-1, 1])
plt.pause(0.1)
bg = fig.canvas.copy_from_bbox(fig.bbox)
ax.draw_artist(line)

fig.canvas.blit(fig.bbox)


file = open("pipe", "rb")
byte = file.read(4*size)
while byte:
    byte = file.read(4*size)
    num2=np.array(struct.unpack("<" + "f" * size, byte))
    convBelt[0:-size]=convBelt[size:]
    convBelt[-size:]=num2

    fig.canvas.restore_region(bg)
    line.set_ydata(convBelt)
    ax.draw_artist(line)
    fig.canvas.blit(fig.bbox)
    fig.canvas.flush_events()
 
