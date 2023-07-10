import numpy as np

c=299 792 458
Tburst=0.064
fc=9.9e9

for i in np.arange(1,5):
    print("echo -e \"$CENTRE, 208, 000000ff, 800000ff, 3, dS=16384 Vr=V0/3\" > coordCirc.txt")
    print("./circ.out >> out.kml")