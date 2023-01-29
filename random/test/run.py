import numpy as np
import matplotlib.pyplot as plt

MODE=int(input())

my_dpi=96
size=2000

   
if MODE==1:
    print(f'MODE:{MODE}')
    print('Közvetelen random függvény')
    r=np.random.rand(size,size)
    """
    real	0m0,720s
    user	0m0,937s
    sys	0m0,476s
    """

if MODE==2:
    print(f'MODE:{MODE}')
    print('Előre foglalt memória egyszerre generált random vektorral töltve')
    r=np.zeros([size,size])
    r0=np.random.rand(size*size)
    for i in range(size):
        r[i,:]=r0[i*size:(i+1)*size]
    """
    real	0m0,736s
    user	0m0,981s
    sys	0m0,426s
    """

if MODE==3:
    print(f'MODE:{MODE}')
    print('Előre foglalt memória egyesével generált random vektorral töltve')
    r=np.zeros([size,size])
    for i in range(size):
        r[i,:]=np.random.rand(size)
    """

    """

if MODE==4:
    print(f'MODE:{MODE}')
    print('Egyesével generált random vektor VSTACK képgenerálással')
    r=np.zeros(size)
    for i in range(size):
        r=np.vstack([r,np.random.rand(size)])
    """
    real	0m21,860s
    user	0m9,983s
    sys	0m12,299s
    """


if MODE==5:
    print(f'MODE:{MODE}')
    print('Egyszerre generált random vektor VSTACK képgenerálással')
    r0=np.random.rand(size*size)
    r=np.zeros(size)
    for i in range(size):
        r=np.vstack([r,r0[i*size:(i+1)*size]])
    '''
    real	0m19,775s
    user	0m10,210s
    sys	0m9,576s
    '''


# plt.figure(figsize=(size/my_dpi, size/my_dpi), dpi=my_dpi)
# plt.imshow(r)
# plt.savefig("fig.png")
# plt.show()
