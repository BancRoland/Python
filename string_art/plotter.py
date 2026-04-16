from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import utils
import math

timestamp="2025_12_14__00_18_33"

folder=f"result/res{timestamp}"
out=np.load(f"./result/res{timestamp}/out.npy")
ring : list[utils.point]
ring=np.load(f"./result/res{timestamp}/ring.npy", allow_pickle=True)


sorted_data = sorted(out, key=lambda x: x[0])
print(sorted_data)


# print(sorted_data)


# image_path = 'zebra.png'
image_path = 'lena.png'

img = Image.open(image_path)
img_array = np.array(img)
img_arraySum=np.sum(img_array, axis=2)
img = utils.Image(img_arraySum)

        
plt.figure()
plt.plot(out,"o-")
plt.grid()
plt.savefig(f"{folder}/out.png")
plt.show()

# for ring_idx_0 in range(NUMBER_OF_POINTS):
#     for ring_idx_1 in range(NUMBER_OF_POINTS):
plt.figure(figsize=[20,15])
img.plot()

for idx,data in enumerate(sorted_data):

    # print(idx)
    sampling_string = utils.string(ring[int(data[1])],ring[int(data[2])])
    # img.plot()
    sampling_string.plot()
    # print(f"{idx}\t{data}")
    if math.isnan(data[0]):
        print(data)
    import time
    # time.sleep(1)
    if not idx%100:
        plt.savefig(f"{folder}/fig_{idx}.png")