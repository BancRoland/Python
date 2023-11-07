import numpy as np
import matplotlib.pyplot as plt

def mandel(c,lmax):
	b=[0+0j, 0+0j]
	for i in range(RANGE):
		b[0]=b[1]
		b[1]=b[0]**2+c
		if abs(b[1]) > lMax:
			return i+1
	return 1
	
	
#my_dpi=96
RANGE=1000	#iterációs mélység -> javít a körvonalakon
lMax=2
res=100
size=0.01
cent=0.358-0.6440j


real=np.linspace(-size,size,res)+np.real(cent)
imag=np.linspace(-size,size,res)+np.imag(cent)
print(min(imag),max(imag),min(real),max(real))


mand2=np.ones((res, res))
idxIM=0
idxRE=0

for im in imag:
	for re in real:
		val=mandel(re+1j*im,lMax)
		mand2[idxIM, idxRE]=val
		idxRE=idxRE+1
	print(idxIM/res*100,"%")
	idxIM=idxIM+1
	idxRE=0

print("done")

plt.figure()
#plt.imshow(np.log10(np.reshape(np.array(mand2),(res, res))), interpolation='nearest', extent=[min(real),max(real),min(imag),max(imag)])
plt.imshow(np.log10(mand2), interpolation='nearest', extent=[min(real),max(real),max(imag),min(imag)])
"""
plt.figure(figsize=(res/my_dpi, res/my_dpi), dpi=my_dpi)
plt.imshow(np.log10(np.array(mand2)), interpolation='nearest', extent=[min(real),max(real),min(imag),max(imag)])
"""
plt.savefig('mandel_TOTRES.png')
plt.grid()
plt.show()

