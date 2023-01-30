#!/usr/bin/env python3

while 1:
    string=input()
    list=string.split()
    nlist=[float(x) for x in list]
    #print('kacsa')
    print(str(nlist[0])+" "+str(nlist[1])+" "+str(nlist[2])+" "+str(nlist[3]))