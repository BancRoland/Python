from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
# sudo apt install python3-pillow

def pair1(x,y,xVal,yVal):
    x1=(xVal-x)%xVal
    y1=(yVal-y)%yVal
    return x1, y1

def pair2(x,y,xVal,yVal):
    x1=(x)%xVal
    y1=(yVal-y)%yVal
    return x1, y1

def corner(i,N):
    if i<N:
        return i, N-1
    else:
        return N-1, (N-1)-(i-N+1)
    
def cShape(i,N):
    if i < N:
        return -N, i+1
    elif i>=N and i<3*N:
        return i-2*N+1, N
    elif i>=3*N and i<4*N:
        return N, 4*N-1-i
    else:
        return 0,0

# Open an image file
# image_path = 'zebra.png'
image_path = 'rails.png'
# image_path = 'galaxy.png'
# image_path = 'glx2.png'
img = Image.open(image_path)

# # Display basic information about the image
# print(f"Image format: {img.format}")
# print(f"Image size: {img.size}")
# print(f"Image mode: {img.mode}")

# Optionally, display the image
# img.show()

img_array = np.array(img)
# img_array = np.zeros([100,100,3])
# img_array = np.random.randn(20,20,3)

# print(np.shape(img_array))      # (1366, 2048, 3)

img_arraySum=np.sum(img_array,axis=2)
# plt.imshow(img_array[:,:,1],cmap="gray")
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



inv=np.fft.ifft2(Fr)

# plt.imshow((np.real(inv)), cmap="gray")
# plt.show()

# plt.imshow((np.real(inv)), cmap="gray")
# plt.show()

dumm=1j*np.zeros(np.shape(Fr))
dumm3=1j*np.zeros(np.shape(Fr))
# dumm2=1j*np.zeros(np.shape(Fr))

N=30
# print(np.shape(Fr))

# for k in range(5):
#     for i in range(2*k-1):
#         print(f"{corner(i,k)} - {pair1(corner(i,k)[0],corner(i,k)[1],np.shape(Fr)[0],np.shape(Fr)[1])}")
#     print()


dumm3[0,0]=Fr[0,0]
dumm[0,0]=Fr[0,0]
for k in range(N):
    for i in range(4*k):
        # print(f"k: {k}  -   i: {i}")
        print(f"{cShape(i,k)} - {pair1(cShape(i,k)[0],cShape(i,k)[1],np.shape(Fr)[0],np.shape(Fr)[1])}")

        x,y=cShape(i,k)
        p1=pair1(x,y,np.shape(Fr)[0],np.shape(Fr)[1])
        # p1=pair1(i,k,np.shape(Fr)[0],np.shape(Fr)[1])
        dumm[x,y]=Fr[x,y]
        dumm[p1[0],p1[1]]=Fr[p1[0],p1[1]]

        dumm3=np.zeros(np.shape(Fr))
        dumm3[x,y]=Fr[x,y]
        dumm3[p1[0],p1[1]]=Fr[p1[0],p1[1]]

        inv=np.fft.ifft2(dumm)
        inv2=np.fft.ifft2(dumm3)

        plt.figure(figsize=[12,6])
        plt.subplot(1,2,1)
        plt.imshow((np.real(inv2)), cmap="gray")
        plt.title("Harmonic component")
        plt.subplot(1,2,2)
        plt.imshow((np.real(inv)), cmap="gray")
        plt.title("Summ of harmonics")

        plt.savefig(f"./out/out_{k}_{i}.png")
        plt.close()

        # plt.subplot(1,3,1)
        # plt.imshow((np.abs(dumm3)), cmap="gray")
        # plt.subplot(1,3,2)
        # plt.imshow((np.real(inv)), cmap="gray")
        # plt.subplot(1,3,3)
        # plt.imshow((np.real(inv2)), cmap="gray")
        # plt.savefig(f"./out/out_{k}_{i}.png")
        # plt.close()
        # print(f"{i*(i+1)/2+j}")
        # plt.show()
    print()


# # for i in range(N):
#     for j in range(i+1):
#         # print(f"{i-j},{j} -   {pair1(i-j,j,np.shape(Fr)[0],np.shape(Fr)[1])}")
#         p1=pair1(i,j,np.shape(Fr)[0],np.shape(Fr)[1])
#         # p2=pair2(i,j,np.shape(Fr)[0],np.shape(Fr)[1])
#         # p3=pair1(p2[0],p2[1],np.shape(Fr)[0],np.shape(Fr)[1])
#         dumm[i,j]=Fr[i,j]
#         dumm[p1[0],p1[1]]=Fr[p1[0],p1[1]]
#         # dumm[p2[0],p2[1]]=Fr[p2[0],p2[1]]
#         # dumm[p3[0],p3[1]]=Fr[p3[0],p3[1]]

#         dumm3=np.zeros(np.shape(Fr))
#         dumm3[i,j]=Fr[i,j]
#         dumm3[p1[0],p1[1]]=Fr[p1[0],p1[1]]
#         # dumm3[p2[0],p2[1]]=Fr[p2[0],p2[1]]
#         # dumm3[p3[0],p3[1]]=Fr[p3[0],p3[1]]

#         inv=np.fft.ifft2(dumm)
#         inv2=np.fft.ifft2(dumm3)
#         plt.subplot(1,3,1)
#         plt.imshow((np.abs(dumm3)), cmap="gray")
#         plt.subplot(1,3,2)
#         plt.imshow((np.real(inv)), cmap="gray")
#         plt.subplot(1,3,3)
#         plt.imshow((np.real(inv2)), cmap="gray")
#         plt.savefig(f"./out/out_{i*(i+1)/2+j}.png")
#         plt.close()
#         print(f"{i*(i+1)/2+j}")
#         # plt.show()