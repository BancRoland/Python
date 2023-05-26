import numpy as np
import matplotlib.pyplot as plt


r=1
R=1.1
G=4
v0=np.arange(0,8,0.01)
vr=np.sqrt(v0**2*(1-r**2/R**2)-2*G*(1/r-1/R))
vt=v0*r/R
v=np.sqrt(vr**2+vt**2)
theta=np.arctan(vr/vt)

vs=np.sqrt(G/R)
v1=vs+np.sqrt((vt-vs)**2+vr**2)
v2=vs+np.sqrt((vt+vs)**2+vr**2)

plt.figure()
plt.plot(v0,'.-')
plt.plot(vr,'.-')
plt.plot(vt,'.-')
plt.plot(v,'.-')
plt.plot(vs,'.-')
plt.plot(v1)
plt.plot(v2)
plt.plot(theta,'.-')
plt.show()

plt.figure()
plt.plot(vt,vr,'.-')
plt.plot(theta,v,'.-')
plt.grid()
plt.show()

plt.polar(theta,v)
plt.show()


# alpha0=47.3
# alpha=alpha0/180*np.pi
# R=6371
# d=42000

# c=np.sqrt(R**2+d**2-2*R*d*np.cos(alpha))   #koszinusztétel
# s=180-np.arcsin(np.sin(alpha)*d/c)/np.pi*180-90

# print(c)
# print(s)