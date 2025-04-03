import numpy as np
import matplotlib.pyplot as plt
import time

def get_checked_outs(out, check_comb):
    checked_outs=np.zeros(len(check_comb)+1)
    checked_outs[-1]=out[-1]
    for i in range(len(check_comb)):
        checked_outs[i]=out[int(check_comb[i])]
    return checked_outs
    

# get the possible combinatons of checking indexes in D flip flop chain
def getChecks(L,num_of_checks):
    out=np.zeros([(L-1)**num_of_checks,num_of_checks])
    for i in range((L-1)**num_of_checks):
        for j in range(num_of_checks):
            val=np.floor(i/((L-1)**j))%(L-1)
            out[i,j]=(val)
    return out
            
def is_sorted(v):
    if np.array_equal(v, np.sort(v)):
        return True
    else:
        return False

def xor(v):
    out=0
    for i in v:
        if i:
            out=out^1
    # print(f'nxor{v} = {out^1}')
    return out

def anyMatch(v):
    for i in range(len(v)):
        for j in range(len(v)):
            if i!=j and v[i]==v[j]:
                return 1
    return 0

def allzero(v):
    for i in range(len(v)):
        if v[i]==1:
            return 0
    return 1

def initVal(v):
    w=np.zeros(len(v))
    w[0]=1
    return w
def isInitVal(v):
    w=initVal(v)
    if np.array_equal(w,v):
        return 1
    else:
        return 0


# print("""
#                                     ---------------------+                
#                                     |                    |    +------+    
#     +---+    +---+           +---+  |           +---+    |----|      |    
#     |   |    |   |           |   |  |           |   |         | NXOR ----|
# |-- | D |--- | D |-- ... --- | D |--+-- ... --- | D |---------|      |   |
# |   |   |    |   |           |   |              |   |         +------+   |
# |   +---+    +---+           +---+              +---+                    |
# |     0        1               N                 L-1                     |
# |                                                                        |
# |                                                                        |
# -------------------------------------------------------------------------|
# """)

print("""                                                                                                         
                                                                                   +------+              
                                    +----------------------------------------------|      |              
                                    |                                              |      |              
                                    |              +-------------------------------|      |              
                                    |              |                            .  |      |              
                                    |              |                            .  |      |              
                                    |              |                            .  | NXOR |------+       
                                    |              |              +----------------|      |      |       
                                    |              |              |                |      |      |       
        +---+   +---+         +---+ |        +---+ |        +---+ |        +---+   |      |      |       
+-------| D |---| D |-- ... --| D |-+- ... --| D |-+- ... --| D |-+- ... --| D |---|      |      |       
|       +---+   +---+         +---+          +---+          +---+          +---+   +------+      |       
|         0       1            C[0]           C[1]          C[G-1]          L-1                  |       
|                                                                                                |       
|                                                                                                |       
|                                                                                                |       
+------------------------------------------------------------------------------------------------+       
""")                                                                                                         

MIN_LEN = 16
MAX_LEN = 16

MIN_GATES = 3
MAX_GATES = 3

PRINT_ONLY_WIN=True
PRINT_FULL_STRING=True



if 1:
    for L in range(MIN_LEN,MAX_LEN+1):
        for G in range(MIN_GATES,min(MAX_GATES+1,L)):  #number of checking positions
            print(f"\nlength(L)= {L}    number of intermediate checking places(G)= {G}")
            print(f"checkIDX(C)\trnd str len\tefficency")
            check_mx=getChecks(L,G)
            for i in range(np.shape(check_mx)[0]):
                check_comb = check_mx[i]
                if not anyMatch(check_comb) and is_sorted(check_comb):
                    # print(check_comb)
                    # out=np.floor(np.random.rand(10)*2)
                    v=np.zeros(0)
                    out=np.zeros(L)
                    out=initVal(out)
                    while True:
                        # print(out)
                        # new=(((((bool(out[-1])^bool(out[CHECK0]))^bool(out[CHECK1]))^bool(out[CHECK2]))^bool(out[CHECK3])))^1
                        # new=(bool(out[-1])^bool(out[CHECK0]))^1
                        checked_outs=get_checked_outs(out,check_comb)
                        new=xor(checked_outs)
                        if 0:
                            print(f"out: {out}")
                            print(f"checked_outs: {checked_outs}")
                            print(f"check_comb: {check_comb}")
                            print(f"new: {new}")
                            print()
                        out=np.concatenate([[new],out[:-1]])
                        v=np.concatenate([v,[new]])
                        if isInitVal(out):
                            break
                    if not PRINT_ONLY_WIN or (len(v) >= (2**L-1)):
                        print(f"{check_comb}\t{len(v)}\t{len(v)/(2**L-1)*100:.4f} %")
                        if PRINT_FULL_STRING:
                            # w=v[::-1]
                            w=v.astype(int)
                            w=np.concatenate([[w[-1]],w[0:-1:]])
                            print(w)
                            np.save("out.npy",w)

if 0:
    v=np.zeros(0)
    out=np.zeros(8)
    print("complex float z[217] = {",end="")
    while True:
        # print(out)
        new=(bool(out[-1])^bool(out[-4]))^1
        out=np.concatenate([[new],out[:-1]])
        v=np.concatenate([v,[new]])
        if allzero(out)==1:
            break
        # print(f"{2*new-1}+0j, ",end="")
        # print(f"{2*new-1}+0*I,",end="")
    print(v)
    print(sum(v)/len(v))

    print("complex float z[217] = {",end="")
    for i in range(len(v)):
        if v[i] == 1:
            print(f"1+0*I",end="")
        else:
            print(f"-1+0*I",end="")
        if i != len(v)-1:
            print(f",",end="")
    print("};")
    
    print()

    # Manchester
    # print("complex float z[434] = {",end="")
    # for i in range(len(v)):
    #     if v[i] == 1:
    #         print(f"0+0*I, 1+0*I",end="")
    #     else:
    #         print(f"1+0*I, 0+0*I",end="")
    #     if i != len(v)-1:
    #         print(f",",end="")
    # print("};")

    print("D=[",end="")
    for i in range(len(v)):
        if v[i] == 1:
            print(f"1+0j",end="")
        else:
            print(f"-1+0j",end="")
        if i != len(v)-1:
            print(f", ",end="")
    print(" ]")

    # Manchester
    # print("D=[",end="")
    # for i in range(len(v)):
    #     if v[i] == 1:
    #         print(f"-1+0j, 1+0j",end="")
    #     else:
    #         print(f"1+0j, -1+0j",end="")
    #     if i != len(v)-1:
    #         print(f", ",end="")
    # print(" ]")

    plt.plot(v,"o-")
    plt.show()

    v=2*v-1

    plt.plot(np.correlate(v,v,"full"),"o-")
    plt.show()

    plt.plot(20*np.log10(np.abs(np.correlate(v,v,"full"))),"o-")
    plt.show()

# # L=9
# # for C1 in range(0,L+1):
# #     for C2 in range(0,C1):
# #         for C3 in range(0,C2):
# #             v=np.zeros(0)
# #             out=np.zeros(L)
# #             while True:
# #                 # new=(((bool(out[-1])^bool(out[C1])))^bool(out[C2]))^1   # C1= 6    C2= 5    len: 254
# #                 # new=((((bool(out[-1])^bool(out[C1])))^(bool(out[0])^bool(out[C2]))))^1  # C1= 6    C2= 5    len: 255
# #                 new=((((bool(out[-1])^bool(out[C1])))^(bool(out[C2])^bool(out[C3]))))^1  # C1= 6    C2= 5    len: 255
# #                 out=np.concatenate([[new],out[:-1]])
# #                 v=np.concatenate([v,[new]])
# #                 # print(out)
# #                 # time.sleep(0.1)
# #                 if allzero(out)==1:
# #                     break
# #             print(f"C1= {C1}    C2= {C2}    C3= {C3}    len: {len(v)}")


# v=np.zeros(0)
# out=np.zeros(9)

# while True:
#     new=(((bool(out[-1])^bool(out[C1])))^bool(out[C2]))^1   # C1= 6    C2= 5    len: 254
#     # new=((((bool(out[-1])^bool(out[C1])))^(bool(out[0])^bool(out[C2]))))^1  # C1= 6    C2= 5    len: 255
#     # new=((((bool(out[-1])^bool(out[1])))^(bool(out[2])^bool(out[3]))))^1  # C1= 6    C2= 5    len: 255
#     # new=((((bool(out[1])^bool(out[3])))^(bool(out[2])^bool(out[-1]))))^1  # C1= 6    C2= 5    len: 255    
#     out=np.concatenate([[new],out[:-1]])
#     v=np.concatenate([v,[new]])
#     # print(out)
#     # time.sleep(0.1)
#     if allzero(out)==1:
#         break

# print(f"len: {len(v)}")
# plt.plot(v,"o-")
# plt.show()

# plt.plot(np.real(np.fft.fft(v-0.5)))
# plt.plot(np.imag(np.fft.fft(v-0.5)))
# plt.plot(np.abs(np.fft.fft(v-0.5)),"--",color="gray",alpha=0.5)
# plt.plot(-np.abs(np.fft.fft(v-0.5)),"--",color="gray",alpha=0.5)
# plt.show()

# plt.plot(np.correlate(v-0.5,v-0.5,"full"))
# plt.show()