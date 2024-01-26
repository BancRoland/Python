import numpy as np

A=10

ArrA=[]

for i in range(A):
    ArrA.append(np.random.randint(0,100,10))
ArrA=np.vstack(ArrA)

print(ArrA)





B=10
ArrB=[]
for i in range(A):
    ArrA=[]
    for j in range(B):
        ArrA.append(np.random.randint(0,100,10))
    ArrA=np.stack(ArrA)
    ArrB.append(ArrA)
ArrB=np.stack(ArrB)

print(np.shape(ArrB))

A = 2
B = 3
C = 5
ArrC = []
for k in range(C):
    ArrB = []
    for i in range(B):
        ArrA = []
        for j in range(A):
            ArrA.append(np.random.randint(0,100,10))

        ArrA = np.stack(ArrA)
        ArrB.append(ArrA)

    ArrB = np.stack(ArrB)
    ArrC.append(ArrB)

ArrC = np.stack(ArrC)

print(np.shape(ArrC))