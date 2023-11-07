import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

data = np.random.rand(100, 400)

# Define a custom colormap with a list of colors
colors_0 = [(0, 0, 0), (1, 0, 0), (1, 1, 0), (1, 1, 1)]  # RGBA values

s=np.arange(0,1024)/1024
r=s
g=(2*s)%1
b=(4*s)%1
colors_Lenart=np.zeros([1024,3])
for i in range(1024):
    colors_Lenart[i,0]=r[i]
    colors_Lenart[i,1]=g[i]
    colors_Lenart[i,2]=b[i]

colors=colors_Lenart

# print(np.shape(colors))
n_bins = 100  # Number of discrete color bins
cmap_name = "custom_colormap"
custom_cmap = mcolors.LinearSegmentedColormap.from_list(cmap_name, colors, N=n_bins)

fig, ax = plt.subplots()
im = ax.imshow(data, cmap=custom_cmap)

cbar = plt.colorbar(im, ax=ax, orientation='vertical')

# Customize the colorbar appearance
cbar.set_label('Custom Colorbar Label')
cbar.set_ticks([0, 0.25, 0.5, 0.75, 1])  # Define custom tick positions
cbar.set_ticklabels(['Low', 'Medium', 'High', 'Very High', 'Max'])  # Define custom tick labels

plt.show()
