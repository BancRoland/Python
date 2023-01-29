import matplotlib.pyplot as plt
import hashlib
import struct


buffer_size=2**10*8
filename="pipe"
file_hash = hashlib.sha256()
with open(filename, mode="rb") as f:
    chunk = f.read(buffer_size)
    while chunk:
        file_hash.update(chunk)
        chunk = f.read(buffer_size)
        print(len(chunk))
        print(type(chunk))
        #print(struct.unpack('i', fin.read(4)))
        #print(struct.unpack('i', fin.read(4)))
        
print(struct.unpack('i', fin.read(4)))
