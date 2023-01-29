import matplotlib.pyplot as plt
import numpy as np
import struct

# def convI32(v):
# 	num=v[3]+256*v[2]+256**2*v[1]+256**3*v[0]
# 	return num

# def dd(v):
# 	return(v*2)

size=2**4
lngt=10	#futószalag hossza
convBelt0=np.zeros(size*lngt)
convBelt1=np.zeros(size*lngt)
convBelt2=np.zeros(size*lngt)
convBelt3=np.zeros(size*lngt)
y=np.arange(size*lngt,0,-1)

fig, ax = plt.subplots()
(line0,) = ax.plot(y, convBelt0, animated=True)
(line1,) = ax.plot(y, convBelt1, animated=True)
(line2,) = ax.plot(y, convBelt2, animated=True)
(line3,) = ax.plot(y, convBelt3, animated=True)

plt.show(block=False)
plt.xlabel('minta')
plt.ylabel('érték')
plt.title('Egérutasítások ábrázolása')
plt.gca().invert_xaxis()
plt.grid()
plt.ylim([-1, 1])
plt.pause(0.1)
bg = fig.canvas.copy_from_bbox(fig.bbox)
ax.draw_artist(line0)
ax.draw_artist(line1)
ax.draw_artist(line2)
ax.draw_artist(line3)
fig.canvas.blit(fig.bbox)


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




    # convBelt0[size:]=convBelt0[0:-size]
    # convBelt0[:size]=num2[0::4]/2**3

    # convBelt1[size:]=convBelt1[0:-size]
    # convBelt1[:size]=num2[1::4]/2**7

    # convBelt2[size:]=convBelt2[0:-size]
    # convBelt2[:size]=num2[2::4]/2**7

    # convBelt3[size:]=convBelt3[0:-size]
    # convBelt3[:size]=num2[3::4]/2**1


    fig.canvas.restore_region(bg)
    line0.set_ydata(convBelt0)
    line1.set_ydata(convBelt1)
    line2.set_ydata(convBelt2)
    line3.set_ydata(convBelt3)
    ax.draw_artist(line0)
    ax.draw_artist(line1)
    ax.draw_artist(line2)
    ax.draw_artist(line3)
    fig.canvas.blit(fig.bbox)
    fig.canvas.flush_events()
    

    """
    plt.ion()
    plt.clf()
    plt.plot(num2)
    plt.ylim([-1, 1])
    plt.show()
    plt.pause(.000001)
    """
