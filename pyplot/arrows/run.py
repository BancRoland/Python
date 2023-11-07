import matplotlib.pyplot as plt

# Create the quiver plot with a single arrow
plt.quiver(0, 0, 1, 1, angles='xy', scale_units='xy', scale=1,color="C0")
plt.quiver(0, 0, 1, 1, scale_units='xy', scale=1,color="C1")
plt.quiver(0, 0, 1, 1, angles='xy', scale=1,color="C2")
plt.quiver(0, 0, 1, 1, angles='xy', scale_units='xy',color="red")
plt.quiver(0, 0, -1, -1,color="yellow")
plt.legend()

plt.quiver(0.5, -0.5, 1, 1, angles='xy', scale_units='xy', scale=1,color="C0")
plt.quiver(0.5, -0.5, 1, 1, scale_units='xy', scale=1,color="C1")
plt.quiver(0.5, -0.5, 1, 1, angles='xy', scale=1,color="C2")
plt.quiver(0.5, -0.5, 1, 1, angles='xy', scale_units='xy',color="red")
plt.quiver(0.5, -0.5, -1, -1,color="yellow")

# Set the limits to ensure the arrow is fully visible
plt.xlim([-2,2])
plt.ylim([-2,2])
plt.gca().set_aspect('equal')
plt.grid()

plt.show()



# import numpy as np
# import matplotlib.pyplot as plt

# plt.figure()
# plt.quiver([0,0],[0,1])
# # plt.quiver([0,0],[-0.1,-0.1])
# # plt.quiver([0,0],[-0.01,0])

# plt.grid()
# # plt.axis("equal")
# plt.xlim([-2,2])
# plt.ylim([-2,2])
# plt.gca().set_aspect('equal')
# plt.show()