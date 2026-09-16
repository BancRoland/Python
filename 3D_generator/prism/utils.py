import matplotlib.pyplot as plt
from dataclasses import dataclass

@dataclass
class Drawing():
    points: list
    name: str

    def plot_my_drawing(self):
        self.points.append(self.points[0])
        for idx in range(len(self.points)-1):
            A=self.points[idx]
            B=self.points[idx+1]
            plt.plot([A[0],B[0]],[A[1],B[1]],color="black")
        plt.show()