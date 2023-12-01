from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
# sudo apt install python3-pillow

# Open an image file
# image_path = '../zebra.png'
# image_path = '../galaxy.png'
# image_path = 'glx2.png'
image_path = 'chirp.png'
img = Image.open(image_path)

# Display basic information about the image
print(f"Image format: {img.format}")
print(f"Image size: {img.size}")
print(f"Image mode: {img.mode}")

# Optionally, display the image
# img.show()

img_array = np.array(img)
# img_array = np.zeros([100,100,3])
# img_array = np.random.randn(10,10,3)

# print(np.shape(img_array))      # (1366, 2048, 3)

img_arraySum=np.sum(img_array,axis=2)
# # plt.imshow(img_array[:,:,1],cmap="gray")
# plt.imshow(img_arraySum,cmap="gray")
# plt.show()

Fr=np.fft.fft2(img_arraySum)

# plt.imshow(np.abs(Fr), cmap="gray")
# plt.show()

# plt.imshow(np.log10(np.fft.fftshift(np.abs(Fr))), cmap="gray")
# plt.show()

# Fr[5,1]=1e9

# plt.imshow(np.log10((np.abs(Fr))), cmap="gray")
# plt.show()





# plt.imshow((np.real(inv)), cmap="gray")
# plt.show()

# plt.imshow((np.real(inv)), cmap="gray")
# plt.show()

corr=Fr*np.conj(Fr)

inv=np.fft.ifft2(corr)

plt.subplot(1,2,1)
plt.imshow(img_arraySum,cmap="gray")
plt.subplot(1,2,2)
plt.imshow(np.log10(np.fft.fftshift(np.real(inv))), cmap="gray")
plt.show()