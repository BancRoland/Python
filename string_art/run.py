from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
# sudo apt install python3-pillow
import utils
from datetime import datetime
import os

timestamp = datetime.now().strftime("%Y_%m_%d__%H_%M_%S")
folder=f"result/res{timestamp}"
os.makedirs(folder, exist_ok=True)

NUMBER_OF_POINTS = 240
NUMBER_OF_SAMPLING_POINTS=100

# Open an image file
# image_path = 'zebra.png'
image_path = 'lena.png'

img = Image.open(image_path)
img_array = np.array(img)
img_arraySum=np.sum(img_array, axis=2)

height,width=np.shape(img_arraySum)
if height<width:
    critical=height
else:
    critical=width
radius=np.floor(critical/2)
img = utils.Image(img_arraySum)

RADIUS = radius-1



A = utils.point(radius,radius)

# plt.figure()


# A.plot()

ring_idx_0 = 0

ring_idx_1 = 5


ring = A.get_circle(r=RADIUS,N=NUMBER_OF_POINTS)

string_num = NUMBER_OF_POINTS*(NUMBER_OF_POINTS-1)/2

cntr=-1
out=[]
for ring_idx_0 in range(0,NUMBER_OF_POINTS-1):
    for ring_idx_1 in range(ring_idx_0+1,NUMBER_OF_POINTS):
        cntr=cntr+1
        if not (cntr % int(string_num/100)):
            print(f"{cntr/string_num*100:.0f}%")

        rpA = ring_idx_0
        rpB = ring_idx_1

        # print(f"{rpA} - {rpB}")
        

        sampling_string = utils.string(ring[rpA],ring[rpB])
        # samlping_points = sampling_string.get_inter(N=NUMBER_OF_SAMPLING_POINTS)
        samlping_points = sampling_string.get_inter_radius(d=10)


        cross_section=img.get_samples(samlping_points)
        sum=img.get_sampleval(samlping_points)
        out.append([sum,rpA,ring_idx_1])
        # out.append(sum)
        # print(sum)

        # plt.subplot(2,1,1)

        # for i in ring:
        #     i.plot()

        # for i in samlping_points:
        #     i.plot()

        PLOT=0
        if PLOT:
            img.plot()
            sampling_string.plot()
            plt.title(f"{sum:.1f}")
            plt.subplot(2,1,2)
            plt.plot(cross_section)
            plt.savefig(f"{folder}/checkp_{cntr}__{rpA}_{rpB}")
            plt.close()

            # plt.show()

np.save(f"{folder}/ring.npy", ring)
np.save(f"{folder}/out.npy",out)

print(timestamp)

