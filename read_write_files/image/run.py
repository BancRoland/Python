from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
# sudo apt install python3-pillow

# Open an image file
image_path = 'zebra.png'
img = Image.open(image_path)

# Display basic information about the image
print(f"Image format: {img.format}")
print(f"Image size: {img.size}")
print(f"Image mode: {img.mode}")

# Optionally, display the image
# img.show()

img_array = np.array(img)

# print(np.shape(img_array))      # (1366, 2048, 3)

img_arraySum=np.sum(img_array,axis=2)
# plt.imshow(img_array[:,:,1],cmap="gray")
plt.imshow(img_arraySum,cmap="gray")
plt.show()
