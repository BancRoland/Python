import matplotlib.pylab as plt  
from dataclasses import dataclass
import numpy as np

def wtf():
    print("wtf")

@dataclass
class point:
    x: float
    y: float

    def __init__(self, X: float, Y: float):
        self.x = X
        self.y = Y

    def __add__(self, other):
        if not isinstance(other, point): 
            return NotImplemented
        new_x=self.x+other.x
        new_y=self.y+other.y
        out=point(new_x,new_y)
        return out

    def plot(self):
        plt.scatter(self.x,self.y)

    def get_len(self)-> float:
        c = np.sqrt(np.abs(self.x**2+self.y**2))
        return c

    def get_circle(self, r: float, N: int)->list["point"]:
        if N<=0:
            raise

        degstep=2*np.pi/N
        out=[]
        for i in range(N):
            alpha = i*degstep
            x=r*np.cos(alpha)
            y=r*np.sin(alpha)
            C = point(x,y)
            out.append(C+self)
        return out
    
    def __truediv__(self, A: int):
        if isinstance(A, (int, float)):
            return point(self.x / A, self.y / A)
        return NotImplemented
    
    def __mul__(self, A):

        # Scalar multiplication
        if isinstance(A, (int, float)):
            return point(self.x * A, self.y * A)
        return NotImplemented
    __rmul__ = __mul__

    def __sub__(self, other):
        if isinstance(other, point):
            return point(self.x - other.x, self.y - other.y)
        return NotImplemented





@dataclass
class string:
    start: point
    end: point

    def get_diff(self):
        diff=self.end-self.start
        return diff

    def get_len(self)-> float:
        diff=self.get_diff()
        c = diff.get_len()
        return c
    
    def get_inter(self, N: int)-> list[point]:
        diff=self.get_diff()
        out=[]
        for i in range(N+1):
            out.append(self.start+diff/N*i)
        return out
    
    def get_inter_radius(self, d: float)-> list[point]:
        diff=self.get_diff()
        len=diff.get_len()
        points_in_len=int(np.floor(len/d))

        step_vec = diff/len*d

        out=[]
        for i in range(points_in_len):
            out.append(self.start+i*step_vec)
        return out
    
    def plot(self):
        plt.plot([self.start.x, self.end.x], [self.start.y, self.end.y], linestyle="-", linewidth=0.1, color="black")






@dataclass
class pixel:
    p: point
    value: float

    def __init__(self, p: point, value: float):
        self.p = p
        self.value = value

@dataclass
class Image:
    img : list[pixel]
    def __init__(self,img : list[pixel]):
        if len(np.shape(img)) != 2:
            raise
        self.img = img

    def plot(self):
        # plt.imshow(self.img,cmap="gray",alpha=0.0)
        plt.gca().invert_yaxis()   # Flip the y-axis
        plt.gca().set_aspect('equal', adjustable='box')


    def get_samples(self, sampling_points: list[point])->list[float]:
        out=[]
        for i in sampling_points:
            x = int(np.floor(i.x))
            y = int(np.floor(i.y))
            out.append(self.img[y, x])  # Note: row=y, col=x for numpy arrays
        return out
    
    def get_sampleval(self, sampling_points: list[point])->float:
        cross_section = self.get_samples(sampling_points)
        NUMBER_OF_SAMPLING_POINTS = len(sampling_points)
        sum = np.sum(cross_section)/NUMBER_OF_SAMPLING_POINTS
        return sum


# @dataclass
# class Image:
#     img : np.ndarray
#     def __init__(self,img : np.ndarray):
#         if len(np.shape(img)) != 2:
#             raise
#         self.img = img

#     def plot(self):
#         plt.imshow(self.img,cmap="gray")




