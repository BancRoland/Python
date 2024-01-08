from scipy.optimize import root
import math

def eqn(x):
    return x + math.cos(x)

myroot = root(eqn,0)

print(myroot.x)