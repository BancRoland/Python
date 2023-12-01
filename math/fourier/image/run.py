from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
# sudo apt install python3-pillow

# Open an image file
image_path = 'zebra.png'
# image_path = 'galaxy.png'
# image_path = 'glx2.png'
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
# plt.imshow(img_array[:,:,1],cmap="gray")
plt.imshow(img_arraySum,cmap="gray")
plt.show()

Fr=np.fft.fft2(img_arraySum)

# plt.imshow(np.abs(Fr), cmap="gray")
# plt.show()

# plt.imshow(np.log10(np.fft.fftshift(np.abs(Fr))), cmap="gray")
# plt.show()

# Fr[5,1]=1e9

# plt.imshow(np.log10((np.abs(Fr))), cmap="gray")
# plt.show()



inv=np.fft.ifft2(Fr)

# plt.imshow((np.real(inv)), cmap="gray")
# plt.show()

# plt.imshow((np.real(inv)), cmap="gray")
# plt.show()

dumm=1j*np.zeros(np.shape(Fr))
dumm2=1j*np.zeros(np.shape(Fr))

N=20
for i in range(N):
    for j in range(N):
        dumm[i,j]=Fr[i,j]
        dumm[-1-i,j]=Fr[-1-i,j]
        dumm[i,-1-j]=Fr[i,-1-j]
        dumm[-1-i,-1-j]=Fr[-1-i,-1-j]

# for i in range(100):
#     dumm[i,0:i]=Fr[i,0:i]
#     dumm[0:i,i]=Fr[0:i,i]

dumm2[0:N,0:N]=Fr[0:N,0:N]
dumm2[-N:,-N:]=Fr[-N:,-N:]
dumm2[0:N,-N:]=Fr[0:N,-N:]
dumm2[-N:,0:N]=Fr[-N:,0:N]


print()


inv=np.fft.ifft2(dumm)
inv2=np.fft.ifft2(dumm2)
plt.subplot(2,2,1)
plt.imshow((np.abs(inv)), cmap="gray")
plt.subplot(2,2,2)
plt.imshow((np.abs(inv2)), cmap="gray")
plt.subplot(2,2,3)
plt.imshow(np.log10(np.abs(dumm)), cmap="gray")
plt.subplot(2,2,4)
plt.imshow(np.log10(np.abs(dumm2)), cmap="gray")
plt.show()