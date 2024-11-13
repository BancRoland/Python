import rawpy
from PIL import Image
import numpy as np

# Define the file paths
input_file = '/home/roland/Desktop/telapo/101D3500/DSC_0001.NEF'
output_file = 'DSC_0001.png'

print("START0")

# Open the NEF file
with rawpy.imread(input_file) as raw:
    # Process the NEF file to get an RGB image
    rgb0 = raw.postprocess(use_camera_wb=True)  # half_size reduces memory usage

print("START1")

# print(rgb.shape)
# for i in range(1000,1100):
#     for j in range(1000,1100):
#         rgb[i,j,:] = 255

rgb=np.array(rgb0, dtype=int)

print("START2")



shape = np.shape(rgb)
size = shape[0] * shape[1]


powercalculation = 0
if powercalculation:
    # print(shape)
    # POWER = 0
    # for i in range(shape[0]):
    #     for j in range(shape[1]):
    #         # print(f"{rgb[i,j,0]}    {rgb[i,j,1]}    {rgb[i,j,2]}")
    #         POWER = POWER + (rgb[i,j,0]**2 + rgb[i,j,1]**2 + rgb[i,j,2]**2)
    #         # print(f"{rgb[i,j,0]**2 + rgb[i,j,1]**2 + rgb[i,j,2]**2} {POWER}")
    #     if i % 100 == 0:
    #         print(f"{i}/{shape[0]}  {POWER}")

    # print(POWER)

    POWER=np.sum(rgb[:,:,:]**2)

    print("START3")


    # print(np.sum(rgb[:,:,0]**2))
    # print(np.sum(rgb[:,:,1]**2))
    # print(np.sum(rgb[:,:,2]**2))

    print(np.sqrt(np.sum(rgb[:,:,0]**2)/size/3))
    print(np.sqrt(np.sum(rgb[:,:,1]**2)/size/3))
    print(np.sqrt(np.sum(rgb[:,:,2]**2)/size/3))

    max_count = np.count_nonzero(rgb == 255)
    min_count = np.count_nonzero(rgb == 0)
    max = np.max(rgb)
    min = np.min(rgb)

    print(f"AVG POWER = {np.sqrt(POWER/size/3):.2f}")
    print(f"max_count={max_count}\tyield = {max_count/size*100:.2f} %")
    print(f"min_count={min_count}\tyield = {min_count/size*100:.2f} %")
    print(f"max = {max}")
    print(f"min = {min}")


saveimage = 0
if saveimage:
    # Convert the processed image to a Pillow Image object
    image = Image.fromarray(rgb)

    # Save the image as a PNG file
    image.save(output_file)

    print("Conversion successful: DSC_0001.NEF to DSC_0001.png")
