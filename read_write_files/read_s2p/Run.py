import skrf
import numpy as np
import matplotlib.pyplot as plt

# Read the S2P file
ntwk = skrf.Network('CH1.S2P')
signal0 = ntwk.s
signal=signal0[:,1,0]
f = ntwk.f

print(np.shape(signal))
plt.plot(f/1e6, np.real(signal))
plt.plot(f/1e6, np.imag(signal))
plt.plot(f/1e6, np.abs(signal), color="gray", alpha=0.5)
plt.grid()
plt.xlabel("frequency [MHz]")
plt.ylabel("amplitude []")
plt.xlim([474,694])
plt.show()
