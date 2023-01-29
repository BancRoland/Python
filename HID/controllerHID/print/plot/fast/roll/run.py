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
convBelt4=np.zeros(size*lngt)
convBelt5=np.zeros(size*lngt)
convBelt6=np.zeros(size*lngt)
convBelt7=np.zeros(size*lngt)
y=np.arange(size*lngt,0,-1)

fig, ax = plt.subplots()
(line0,) = ax.plot(y, convBelt0, animated=True)
(line1,) = ax.plot(y, convBelt1, animated=True)
(line2,) = ax.plot(y, convBelt2, animated=True)
(line3,) = ax.plot(y, convBelt3, animated=True)
(line4,) = ax.plot(y, convBelt4, animated=True)
(line5,) = ax.plot(y, convBelt5, animated=True)
(line6,) = ax.plot(y, convBelt6, animated=True)
(line7,) = ax.plot(y, convBelt7, animated=True)

plt.show(block=False)
plt.xlabel('minta')
plt.ylabel('érték')
plt.title('Egérutasítások ábrázolása')
plt.gca().invert_xaxis()
plt.grid()
plt.ylim([0, 256])
major_ticks = np.arange(0, 256, 64)
minor_ticks = np.arange(0, 256, 8)

ax.set_yticks(major_ticks)
ax.set_yticks(minor_ticks, minor=True)

plt.pause(0.1)
bg = fig.canvas.copy_from_bbox(fig.bbox)
ax.draw_artist(line0)
ax.draw_artist(line1)
ax.draw_artist(line2)
ax.draw_artist(line3)
ax.draw_artist(line4)
ax.draw_artist(line5)
ax.draw_artist(line6)
ax.draw_artist(line7)





fig.canvas.blit(fig.bbox)


file = open("pipe", "rb")
byte = file.read(8*size)
while byte:
    byte = file.read(8*size)
    num2=np.array(struct.unpack("<" + "B" * size * 8 , byte))
    # print(num2)
    # print(f'M1  M2  M3  M4')
    # print(f'M1: {num2[0::4]}   M2:  {num2[1::4]}   M3:  {num2[2::4]}   M4   {num2[3::4]}')
    # print("----")
    
    print(f'M1: {num2[0::8]}   M2:  {num2[1::8]}   M3:  {num2[2::8]}   M4   {num2[3::8]}   M1: {num2[4::8]}   M2:  {num2[5::8]}   M3:  {num2[6::8]}   M4   {num2[7::8]}')
    print("----")

    convBelt0[0:-size]=convBelt0[size:]
    convBelt0[-size:]=num2[0::8]/2**0

    convBelt1[0:-size]=convBelt1[size:]
    convBelt1[-size:]=num2[1::8]/2**0

    convBelt2[0:-size]=convBelt2[size:]
    convBelt2[-size:]=num2[2::8]/2**0

    convBelt3[0:-size]=convBelt3[size:]
    convBelt3[-size:]=num2[3::8]/2**0


    convBelt4[0:-size]=convBelt4[size:]
    convBelt4[-size:]=num2[4::8]/2**0
    
    
    convBelt5[0:-size]=convBelt5[size:]
    convBelt5[-size:]=num2[5::8]/2**0
    
    
    convBelt6[0:-size]=convBelt6[size:]
    convBelt6[-size:]=num2[6::8]/2**0
    
    
    convBelt7[0:-size]=convBelt7[size:]
    convBelt7[-size:]=num2[7::8]/2**0


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
    line4.set_ydata(convBelt4)
    line5.set_ydata(convBelt5)
    line6.set_ydata(convBelt6)
    line7.set_ydata(convBelt7)
    ax.draw_artist(line0)
    ax.draw_artist(line1)
    ax.draw_artist(line2)
    ax.draw_artist(line3)
    ax.draw_artist(line4)
    ax.draw_artist(line5)
    ax.draw_artist(line6)
    ax.draw_artist(line7)
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
