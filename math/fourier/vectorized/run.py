import numpy as np
import matplotlib.pyplot as plt

vector = np.array([1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0])
plt.plot(vector)
vector_res = vector.reshape(6,10)
print(vector_res)

spec=np.fft.fft(vector_res, axis=1)

print(spec)

correlation_length = 6

number_of_iterations = len(vector)//correlation_length
surv_reshaped = (vector[0:(number_of_iterations * correlation_length)]).reshape(correlation_length, number_of_iterations)
surv_reshaped0   = vector[0: correlation_length]

print(f"wtf {np.sum(surv_reshaped0-surv_reshaped[:,0])}")
print(surv_reshaped0)
print(surv_reshaped)
print(surv_reshaped[:,0])
