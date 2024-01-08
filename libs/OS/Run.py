import numpy as np
import os
from os.path import join
import matplotlib.pyplot as plt

for i in range(5):
    for j in range(5):
        print(f'{i} - {j}')

meas_root_path = "/home/bancr/Desktop/pointer/measurement"
meas_id = 2
# meas_path = os.path.join(meas_root_path,"{:04d}".format(meas_id))
# meas_path = os.path.join(meas_root_path,f"{meas_id:04d}")
# meas_path = np.join(meas_root_path,f"{meas_id:04d}")
meas_path = os.path.join("cica","Kutya")
meas_path = join("cica","Kutya")

x=np.arange(1,4,0.1)
fig=plt.plot(x,x**2)
# plt.show()
img_bytes = fig.to_image(format="png", width=1000, height=1000)

rd_matrix_file = open("/home/bancr/Desktop/Python/OS", 'wb')
rd_matrix_file.write(img_bytes)
rd_matrix_file.close()

print(meas_path)