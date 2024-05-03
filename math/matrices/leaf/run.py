import numpy as np
import matplotlib.pyplot as plt

A=np.exp(1j*np.arange(100)/100*2*np.pi)
B=np.array([np.real(A),np.imag(A)])
print(B)
# plt.scatter(B[0],B[1])
# plt.grid()
# plt.gca().set_aspect('equal', adjustable='box')
# plt.show()

M = np.array([[1, 0], [1, 1]])
# M = np.array([[0, 0], [0, 1]])
eigenvalues, eigenvectors = np.linalg.eig(M)
print(eigenvalues)
print(eigenvectors)
b = -1*(M[0,0]+M[1,1])
a = 1
c = M[1,1]*M[0,0]-M[0,1]*M[1,0]
print((-b+np.sqrt(b**2-4*a*c))/2/a)
print((-b-np.sqrt(b**2-4*a*c))/2/a)

d=100

# plt.figure(figsize=(10,10))
for i in range(d):
    alpha=i/d*np.pi*2
    # v=np.reshape(np.array(np.cos(alpha),np.sin(alpha)),[1,-1])
    v=np.array([np.cos(alpha),np.sin(alpha)]).reshape(-1, 1)
    plt.scatter(v[0,0],v[1,0],color="C0")
    w=M@v
    plt.scatter(w[0,0],w[1,0],color="C1")
    # plt.arrow(v[0,0],v[0,1], w[0,0] - v[0,0], ws[0,1] - v[0,1], head_width=0.1, head_length=0.2, fc='red', ec='red')
    plt.annotate('', xy=(v[0,0], v[1,0]), xytext=(0, 0), arrowprops=dict(color='C0',arrowstyle="->"))
    plt.annotate('', xy=(w[0,0], w[1,0]), xytext=(v[0,0], v[1,0]), arrowprops=dict(facecolor='black',arrowstyle="->"))
plt.annotate('', xy=(eigenvectors[0,0], eigenvectors[1,0]), xytext=(0, 0), arrowprops=dict(color='C3',arrowstyle="->"))
plt.annotate('', xy=(eigenvectors[0,1], eigenvectors[1,1]), xytext=(0, 0), arrowprops=dict(color='C3',arrowstyle="->"))

# plt.scatter(eigenvectors[0,0],eigenvectors[0,1],color="C3")
# plt.scatter(eigenvectors[1,0],eigenvectors[1,1],color="C3")
R1=M@eigenvectors[:,0]
plt.scatter(R1[0],R1[1],color="C4")
R2=M@eigenvectors[:,1]
plt.scatter(R2[0],R2[1],color="C4")
print(R1)
print(R2)
plt.grid()
plt.axis('equal')
plt.show()








# plt.figure(figsize=(10,10))
for i in range(d):
    alpha=i/d*np.pi*2
    # v=np.reshape(np.array(np.cos(alpha),np.sin(alpha)),[1,-1])
    v=np.array([np.cos(alpha),np.sin(alpha)]).reshape(-1, 1)
    plt.scatter(v[0,0],v[1,0],color="C0")
    w=np.transpose(np.transpose(v)@M)
    plt.scatter(w[0,0],w[1,0],color="C1")
    # plt.arrow(v[0,0],v[0,1], w[0,0] - v[0,0], ws[0,1] - v[0,1], head_width=0.1, head_length=0.2, fc='red', ec='red')
    plt.annotate('', xy=(v[0,0], v[1,0]), xytext=(0, 0), arrowprops=dict(color='C0',arrowstyle="->"))
    plt.annotate('', xy=(w[0,0], w[1,0]), xytext=(v[0,0], v[1,0]), arrowprops=dict(facecolor='black',arrowstyle="->"))
plt.annotate('', xy=(eigenvectors[0,0], eigenvectors[1,0]), xytext=(0, 0), arrowprops=dict(color='C3',arrowstyle="->"))
plt.annotate('', xy=(eigenvectors[0,1], eigenvectors[1,1]), xytext=(0, 0), arrowprops=dict(color='C3',arrowstyle="->"))

# plt.scatter(eigenvectors[0,0],eigenvectors[0,1],color="C3")
# plt.scatter(eigenvectors[1,0],eigenvectors[1,1],color="C3")
R1=np.transpose(eigenvectors[:,0])@M
plt.scatter(R1[0],R1[1],color="C4")
R2=np.transpose(eigenvectors[:,1])@M
plt.scatter(R2[0],R2[1],color="C4")
print(R1)
print(R2)
plt.grid()
plt.axis('equal')
plt.show()








# plt.figure(figsize=(10,10))
for i in range(d):
    alpha=i/d*np.pi*2
    # v=np.reshape(np.array(np.cos(alpha),np.sin(alpha)),[1,-1])
    v=np.array([np.cos(alpha),np.sin(alpha)]).reshape(-1, 1)
    plt.scatter(v[0,0],v[1,0],color="C0")
    w=(np.transpose(v)@M)@v
    plt.scatter(w*v[0,0],w*v[1,0],color="C1")
    # plt.arrow(v[0,0],v[0,1], w[0,0] - v[0,0], ws[0,1] - v[0,1], head_width=0.1, head_length=0.2, fc='red', ec='red')
    plt.annotate('', xy=(v[0,0], v[1,0]), xytext=(0, 0), arrowprops=dict(color='C0',arrowstyle="->"))
    plt.annotate('', xy=(w*v[0,0], w*v[1,0]), xytext=(v[0,0], v[1,0]), arrowprops=dict(facecolor='black',arrowstyle="->"))
plt.annotate('', xy=(eigenvectors[0,0], eigenvectors[1,0]), xytext=(0, 0), arrowprops=dict(color='C3',arrowstyle="->"))
plt.annotate('', xy=(eigenvectors[0,1], eigenvectors[1,1]), xytext=(0, 0), arrowprops=dict(color='C3',arrowstyle="->"))

# plt.scatter(eigenvectors[0,0],eigenvectors[0,1],color="C3")
# plt.scatter(eigenvectors[1,0],eigenvectors[1,1],color="C3")
R1=np.transpose(eigenvectors[:,0])@M
plt.scatter(R1[0],R1[1],color="C4")
R2=np.transpose(eigenvectors[:,1])@M
plt.scatter(R2[0],R2[1],color="C4")
print(R1)
print(R2)
plt.grid()
plt.axis('equal')
plt.show()