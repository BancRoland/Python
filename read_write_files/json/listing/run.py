import json
import numpy as np


data={}
for cpi_i in range(10): # for every cpi file
    amb_val=[]
    for chan_i in [0]: # for only ref_channel (because they are mostly the same)
        for stat_i in range(8): # for every station
            amb_val.append(int(100*np.random.rand(1)))
    key=f"cpi_{cpi_i:04d}_amb"
    data[key]=amb_val


# write into JSON file
with open(f'data.json', 'w') as json_file:
    json_file.write("{\n")
    comma_flag=1
    for key, value in data.items():
        if comma_flag==0:   # if not first line, then start with come+newline
            json_file.write(f',\n')
        else:
            comma_flag=0
        json_file.write(f'\"{key}\": {json.dumps(value)}')
        print(f'\"{key}\": {json.dumps(value)}')
    json_file.write("\n}")


# Read from the JSON file
with open(f'data.json', 'r') as json_file:
    json_content = json_file.read()
    data = json.loads(json_content)
values_2d = [value for value in data.values()]
print(np.shape(values_2d))
print(values_2d)

