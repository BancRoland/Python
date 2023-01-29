import matplotlib.pyplot as plt
import numpy as np
import struct

# def convI32(v):
# 	num=v[3]+256*v[2]+256**2*v[1]+256**3*v[0]
# 	return num

# def dd(v):
# 	return(v*2)

size=2**5
lngt=10	#futószalag hossza
convBelt0=np.zeros(size*lngt)
convBelt1=np.zeros(size*lngt)
convBelt2=np.zeros(size*lngt)
convBelt3=np.zeros(size*lngt)

fig, axes = plt.subplots()
fig.show()
fig.canvas.draw()
axes.set_ylim(-1,1)
axes.set_ylabel('label')
axes.set_title('title')
axes.grid
plt.grid()
plt.title('title')
line0 = axes.plot(convBelt0)[0]
line1 = axes.plot(convBelt1)[0]
line2 = axes.plot(convBelt2)[0]
line3 = axes.plot(convBelt3)[0]
background = fig.canvas.copy_from_bbox(axes.bbox)


file = open("pipe", "rb")
byte = file.read(4*size)
while byte:
    byte = file.read(4*size)
    num2=np.array(struct.unpack("<" + "b" * size * 4 , byte))
    # print(num2)
    # print(f'M1  M2  M3  M4')
    # print(f'M1: {num2[0::4]}   M2:  {num2[1::4]}   M3:  {num2[2::4]}   M4   {num2[3::4]}')
    # print("----")

    convBelt0[0:-size]=convBelt0[size:]
    convBelt0[-size:]=num2[0::4]/2**3

    convBelt1[0:-size]=convBelt1[size:]
    convBelt1[-size:]=num2[1::4]/2**7

    convBelt2[0:-size]=convBelt2[size:]
    convBelt2[-size:]=num2[2::4]/2**7

    convBelt3[0:-size]=convBelt3[size:]
    convBelt3[-size:]=num2[3::4]/2**1


    fig.canvas.restore_region(background)
    line0.set_ydata(convBelt0)
    line1.set_ydata(convBelt1)
    line2.set_ydata(convBelt2)
    line3.set_ydata(convBelt3)
    axes.draw_artist(line0)
    axes.draw_artist(line1)
    axes.draw_artist(line2)
    axes.draw_artist(line3)
    fig.canvas.blit(axes.bbox)

    

    """
    plt.ion()
    plt.clf()
    plt.plot(num2)
    plt.ylim([-1, 1])
    plt.show()
    plt.pause(.000001)
    """
