#!/usr/bin/env python3

print("type in some numbers! ex: \"12.3 4.56 7.89\"")
string=input()
print("string: "+string)

list=string.split()
print("list ")
print(list)

nlist=[float(x) for x in list]
print("numList ")
print(nlist)