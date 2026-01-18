import matplotlib.pyplot as plt
import numpy as np

class crd:
    x: float = 0
    y: float = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return crd(x=self.x + other.x, y = self.y + other.y)

def plt_line(A: crd, B: crd, color = "gray", linewidth = 1, linestyle = ":"):
    plt.plot([A.x,B.x],[A.y,B.y], color = color, linewidth = linewidth, linestyle = linestyle)

def makegrid(x_ticks: list[float], y_ticks: list[float], margin: float =1):

    max_x = max(x_ticks)
    min_x = min(x_ticks)

    max_y = max(y_ticks)
    min_y = min(y_ticks)

    X=min_x-margin
    Y=min_y-margin
    left_bott = crd(X,Y)

    X=min_x-margin
    Y=max_y+margin
    left_top = crd(X,Y)

    X=max_x+margin
    Y=max_y+margin
    right_top = crd(X,Y)

    X=max_x+margin
    Y=min_y-margin
    right_bott = crd(X,Y)

    plt_line(left_bott,left_top, color="white")
    plt_line(left_top, right_top, color="white")
    plt_line(right_top, right_bott, color="white")
    plt_line(right_bott, left_bott, color="white")
    

    for x in x_ticks:
        A = crd(x,min_y)
        B = crd(x,max_y)
        plt_line(A,B)

    for y in y_ticks:
        A = crd(min_x,y)
        B = crd(max_x,y)
        plt_line(A,B)    

def integ(sizes: list[float]):
    out = []
    out.append(0)
    for s in sizes:
        out.append(s+out[-1])
    return np.array(out)

class sewing_pattern:
    x_sizes: list[float] = []
    y_sizes: list[float] = []

    def __init__(self, x_sizes: list[float], y_sizes: list[float]):
        self.x_sizes = x_sizes.copy()
        self.y_sizes = y_sizes.copy()