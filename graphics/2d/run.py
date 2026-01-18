import numpy as np
import matplotlib.pyplot as plt
from utils import *
from patterns import *





pattern = phone_case




x_sizes = pattern.x_sizes
y_sizes = pattern.y_sizes

x_ticks = integ(x_sizes)
y_ticks = integ(y_sizes)

margin = 1
x_size = (max(x_ticks)+2*margin)/2.54
y_size = (max(y_ticks)+2*margin)/2.54


plt.figure(figsize=[x_size, y_size])

makegrid(x_ticks, y_ticks, margin = margin)

plt.xlim([min(x_ticks)-margin,max(x_ticks)+margin])
plt.ylim([min(y_ticks)-margin,max(y_ticks)+margin])
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
plt.axis('off')
plt.savefig("out.pdf", dpi=500, bbox_inches='tight', pad_inches=0)
