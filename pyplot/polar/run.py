import matplotlib.pyplot as plt
import numpy as np

LEN = 100

angle=np.arange(LEN)
value=np.random.rand(LEN)
 
_,ax = plt.subplots(subplot_kw = {'projection': 'polar', 'theta_direction': -1})


ax.set_theta_zero_location("N")
ax.plot(angle, value, 'o', markersize=8, color=f"C0")
ax.plot([0,1],[0,1])
# ax.annotate('', xy=(angle,1), xytext=(0, 0), arrowprops=dict(arrowstyle="->"))
ax.set_rmin(0)
ax.set_rmax(2)
ax.grid(True)
ax.set_xlabel('azimuth [deg]')
ax.set_thetagrids(np.arange(0, 360, 30), labels=None)
ax.legend(loc='lower left', bbox_to_anchor=(-0.3, -0.1))
label_position = 0
ax.text(np.pi/2,(ax.get_rmax() + ax.get_rmin())/2, 'Power [dBFS]', rotation = label_position, ha='center', va='center')

plt.title("Beam power values BCPI")

plt.savefig("phasors.png")
plt.close()