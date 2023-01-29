import matplotlib.pyplot as plt
import struct

def convI32(v):
	num=v[3]+256*v[2]+256**2*v[1]+256**3*v[0]
	return num

def dd(v):
	return(v*2)

total=[]
file = open("mic_2022-12-26_18:06:51.i32", "rb")
byte = file.read(4)
#while byte:
for i in range(50000):
    print(len(byte))
    print(list(byte))
    v=list(byte)
    num=convI32(v)
    print(num)
    byte = file.read(4)
    #print(struct.unpack("<" + "f" * numFloats, dataFromFile))
    num2=struct.unpack("<" + "i" * 1, byte)[0]
    print(num2)
    total.append(num2)
    
plt.plot(total)
plt.show()
