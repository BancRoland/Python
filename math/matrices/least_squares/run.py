import numpy as np

# Given matrices A and b
A = np.array([[1, 2], [3, 4], [5, 6]])
b = np.array([1, 2, 3])

# Compute A^TA and A^Tb
ATA = np.dot(A.T, A)
ATb = np.dot(A.T, b)

# Solve the system A^TAx = A^Tb for x
x_hat = np.linalg.solve(ATA, ATb)

print("The least squares solution x_hat is:", x_hat)
print(A@x_hat)
