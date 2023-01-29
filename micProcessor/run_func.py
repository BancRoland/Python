import matplotlib.pyplot as plt
import hashlib


def get_sha256_hash(filename, buffer_size=2**10*8):
    file_hash = hashlib.sha256()
    with open(filename, mode="rb") as f:
        chunk = f.read(buffer_size)
        while chunk:
            file_hash.update(chunk)
            chunk = f.read(buffer_size)
            print(len(chunk))
    return file_hash.hexdigest()


a=get_sha256_hash('pipe')
print("answer:",len(a))

"""
with open("pipe", mode="rb") as file:
	print(float(file.read()))
"""	
