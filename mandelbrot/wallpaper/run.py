import numpy as np
import matplotlib.pyplot as plt

def mandel(c,lmax,rng):
	b=[0+0j, 0+0j]
	for i in range(rng):
		b[0]=b[1]
		b[1]=b[0]**2+c
		if abs(b[1]) > lMax:
			return i+1
	return 1
	
	
my_dpi=96
lMax=2
rng=400	#iteráció szám
res=2
size=0.1	#képméret
#cent=[-0.14-0.95j, -1.8j+0j]
cent=-1.8+0j
#cent=0.32+0.05j
#cent=0.358-0.6440j
scH=1080*res
scW=1920*res
#scH=200
#scW=400




#real=np.linspace(-size+np.real(cent),size+np.real(cent),res)
#imag=np.linspace(-size+np.imag(cent),size+np.imag(cent),res)



imag=(np.arange(scH)-scH/2)/scH*size+np.imag(cent)
real=(np.arange(scW)-scW/2)/scH*size+np.real(cent)


#print(min(imag),max(imag),min(real),max(real))
#print(len(imag), len(real))


mand2=np.ones((int(scH), int(scW)))
idxIM=0
idxRE=0

for im in imag:
	for re in real:
		val=mandel(re+1j*im,lMax,rng)
		mand2[idxIM, idxRE]=val
		idxRE=idxRE+1
	print("{:.2f}".format(idxIM/scH*100)+"%")
	idxIM=idxIM+1
	idxRE=0

print("done")
"""
plt.figure()
plt.imshow(np.log10(np.reshape(np.array(mand2),(res, res))), interpolation='nearest', extent=[min(real),max(real),min(imag),max(imag)])
"""
#plt.figure(figsize=(3.841, 7.195), dpi=my_dpi)
img=plt.figure(figsize=(scW/my_dpi, scH/my_dpi), dpi=my_dpi, frameon=False)
#img=plt.figure(frameon=False)
#plt.imshow(np.log10(np.array(mand2)), interpolation='nearest', extent=[min(real),max(real),min(imag),max(imag)])
plt.imshow(np.log10(np.array(mand2)), interpolation='nearest')
plt.axis('off')
#picname="madel_c{}+{}i_siz{}_res{}".format(real(cent),imag(cent),size,res)
#print(np.imag(cnt))
picname="madel_c{}+{}i_siz{}_res{}_rng{}".format(np.real(cent),np.imag(cent),size,res,rng)

print(picname)
plt.savefig(picname+".png", bbox_inches='tight', pad_inches = 0, dpi=my_dpi)
plt.set_cmap('jet')
plt.savefig(picname+"_bl.png", bbox_inches='tight', pad_inches = 0, dpi=my_dpi)
plt.show()

