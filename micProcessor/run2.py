file = open("mic_2022-12-24_17:51:22.i32", "rb")
byte = file.read(4)
while byte:
    print(list(byte))
    byte = file.read(4)
   
