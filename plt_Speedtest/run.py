import matplotlib.pyplot as plt
import numpy as np
import time

x = np.arange(100)
y = np.random.rand(100)

fig, axes = plt.subplots()
fig.show()
fig.canvas.draw()

#line = axes.plot(x, y, animated=True)[0]
line = axes.plot(x, y)[0]

background = fig.canvas.copy_from_bbox(axes.bbox)

tstart = time.time()
for i in range(1, 2000):
    fig.canvas.restore_region(background)
    line.set_ydata(np.random.rand(100))
    axes.draw_artist(line)
    fig.canvas.blit(axes.bbox)

print('FPS:' , 2000/(time.time()-tstart))
