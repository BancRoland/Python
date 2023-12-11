import numpy as np
import matplotlib.pyplot as plt
import time

def allzero(v):
    for i in range(len(v)):
        if v[i]==1:
            return 0
    return 1

print("""
                                    ---------------------+                
                                    |                    |    +------+    
    +---+    +---+           +---+  |           +---+    |----|      |    
    |   |    |   |           |   |  |           |   |         | NXOR ----|
|-- | D |--- | D |-- ... --- | D |--+-- ... --- | D |---------|      |   |
|   |   |    |   |           |   |              |   |         +------+   |
|   +---+    +---+           +---+              +---+                    |
|     0        1               N                 L-1                     |
|                                                                        |
|                                                                        |
-------------------------------------------------------------------------|
""")

if 0:
    for L in range(2,9):
        print(f"length= {L}")
        for C in range(L-1):
            CHECK=C
            # out=np.floor(np.random.rand(10)*2)
            v=np.zeros(0)
            out=np.zeros(L)
            while True:
                # print(out)
                new=(bool(out[-1])^bool(out[CHECK]))^1
                out=np.concatenate([[new],out[:-1]])
                v=np.concatenate([v,[new]])
                if allzero(out)==1:
                    break
            print(f"checkIDX {C}    len= {len(v)}")

if 0:
    v=np.zeros(0)
    out=np.zeros(8)
    while True:
        # print(out)
        new=(bool(out[-1])^bool(out[4]))^1
        out=np.concatenate([[new],out[:-1]])
        v=np.concatenate([v,[new]])
        if allzero(out)==1:
            break
    # print(v)
    print(sum(v)/len(v))

    plt.plot(v,"o-")
    plt.show()


    plt.plot(np.correlate(v,v,"full"),"o-")
    plt.show()

# L=8
# for C1 in range(0,L+1):
#     for C2 in range(0,C1):
#         for C3 in range(0,C2):
#             v=np.zeros(0)
#             out=np.zeros(L)
#             while True:
#                 # new=(((bool(out[-1])^bool(out[C1])))^bool(out[C2]))^1   # C1= 6    C2= 5    len: 254
#                 # new=((((bool(out[-1])^bool(out[C1])))^(bool(out[0])^bool(out[C2]))))^1  # C1= 6    C2= 5    len: 255
#                 new=((((bool(out[-1])^bool(out[C1])))^(bool(out[C2])^bool(out[C3]))))^1  # C1= 6    C2= 5    len: 255
#                 out=np.concatenate([[new],out[:-1]])
#                 v=np.concatenate([v,[new]])
#                 # print(out)
#                 # time.sleep(0.1)
#                 if allzero(out)==1:
#                     break
#             print(f"C1= {C1}    C2= {C2}    C3= {C3}    len: {len(v)}")


v=np.zeros(0)
out=np.zeros(8)
while True:
    # new=(((bool(out[-1])^bool(out[C1])))^bool(out[C2]))^1   # C1= 6    C2= 5    len: 254
    # new=((((bool(out[-1])^bool(out[C1])))^(bool(out[0])^bool(out[C2]))))^1  # C1= 6    C2= 5    len: 255
    # new=((((bool(out[-1])^bool(out[1])))^(bool(out[2])^bool(out[3]))))^1  # C1= 6    C2= 5    len: 255
    new=((((bool(out[1])^bool(out[3])))^(bool(out[2])^bool(out[-1]))))^1  # C1= 6    C2= 5    len: 255    
    out=np.concatenate([[new],out[:-1]])
    v=np.concatenate([v,[new]])
    # print(out)
    # time.sleep(0.1)
    if allzero(out)==1:
        break

print(f"len: {len(v)}")
plt.plot(v,"o-")
plt.show()

plt.plot(np.real(np.fft.fft(v-0.5)))
plt.plot(np.imag(np.fft.fft(v-0.5)))
plt.plot(np.abs(np.fft.fft(v-0.5)),"--",color="gray",alpha=0.5)
plt.plot(-np.abs(np.fft.fft(v-0.5)),"--",color="gray",alpha=0.5)
plt.show()

plt.plot(np.correlate(v-0.5,v-0.5,"full"))
plt.show()