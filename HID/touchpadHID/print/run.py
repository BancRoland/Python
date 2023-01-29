import matplotlib.pyplot as plt
import numpy as np
import struct

# def convI32(v):
# 	num=v[3]+256*v[2]+256**2*v[1]+256**3*v[0]
# 	return num

# def dd(v):
# 	return(v*2)

size=2**0

# fig, axes = plt.subplots()
# fig.show()
# fig.canvas.draw()
# line = axes.plot(np.zeros(size))[0]
# background = fig.canvas.copy_from_bbox(axes.bbox)


file = open("pipe", "rb")
byte = file.read(4*size)
while byte:
    byte = file.read(4*size)
    # print(f'M1  M2  M3  M4')
    # print(f'{byte[0::4]}   {byte[1::4]}   {byte[2::4]}   {byte[3::4]}')
    # print("----")

    num2=np.array(struct.unpack("<" + "b" * size * 4 , byte))
    #print(num2)
    #print(f'M1  M2  M3  M4')
    print(f'M1: {num2[0::4]}   M2:  {num2[1::4]}   M3:  {num2[2::4]}   M4   {num2[3::4]}')
    print("----")

    # fig.canvas.restore_region(background)
    # line.set_ydata(num2)
    # axes.draw_artist(line)
    # fig.canvas.blit(axes.bbox)


    # plt.ion()
    # plt.clf()
    # plt.plot(byte[0::4])
    # plt.plot(byte[1::4])
    # plt.plot(byte[2::4])
    # plt.plot(byte[3::4])
    # # plt.ylim([-1, 1])
    # plt.show()
    # plt.pause(.000001)
