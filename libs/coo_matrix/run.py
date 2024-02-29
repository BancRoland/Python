from scipy.sparse import coo_matrix
import numpy as np
import matplotlib.pyplot as plt
from icecream import ic 

# Example matrix creation with consistent lengths
row = [0, 1, 2]
col = [0, 1, 2]
data = [1, 2, 3]

sparse_matrix = coo_matrix((data, (row, col)))
ic(sparse_matrix)

print(np.shape(sparse_matrix))
print(sparse_matrix.data)

dense_matrix = sparse_matrix.toarray()

plt.imshow(dense_matrix)
plt.show()