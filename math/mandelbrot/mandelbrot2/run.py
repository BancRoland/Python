import numpy as np
import matplotlib.pyplot as plt

def mandel(c,lmax):
	b=[0+0j, 0+0j]
	for i in range(20):
		b[0]=b[1]
		b[1]=b[0]**2+c
		if abs(b[1]) > lMax:
			return i+1
	return 1
	
	

lMax=2	#ez elvileg valami tétel
res=1000
size=2
cent=-0+0j


real=np.linspace(-size+np.real(cent),size+np.real(cent),res)
imag=np.linspace(-size+np.imag(cent),size+np.imag(cent),res)
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
"""
plt.imshow(np.log10(np.reshape(np.array(mand2),(res, res))), interpolation='nearest', extent=[min(real),max(real),min(imag),max(imag)])
"""

plt.imshow(np.log10(np.array(mand2)), interpolation='nearest', extent=[min(real),max(real),min(imag),max(imag)])
plt.savefig('mandel4.png')
plt.show()

