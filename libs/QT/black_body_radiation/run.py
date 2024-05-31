import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QSlider, QLabel
from PyQt5.QtCore import Qt
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

T=5778
k_B=1.380649E-23 #[J/K] Boltzmann állandó
R_S=696_340_000 #[m] földtávolság
R_T=150E9 #[m] földtávolság

A_S=4*R_S**2*np.pi
A_T=4*R_T**2*np.pi

c=3E8 #[m/s] speed of light
h=6.62607015E-34 #[J/Hz]
sigma=5.67E-8   #[W/m^2/K^4]

T=5778  #[K]


# y = ax^2 + bx + c

Min_A_Val = -100
Min_B_Val = -100
Min_T_Val = 1

Max_A_Val = 100
Max_B_Val = 100
Max_T_Val = 10000

Default_A_Value = 1
Default_B_Value = 0
Default_T_Value = T

tick_interval = 1

A_scale_factor = 0.001
B_scale_factor = 0.01
C_scale_factor = 1


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Create a layout
        layout = QVBoxLayout(self)

        # Create a matplotlib figure and add it to the layout
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)


        # # A
        # # Create a phase slider and set its range
        # self.A_slider = QSlider(Qt.Horizontal)
        # self.A_slider.setRange(Min_A_Val, Max_A_Val)
        # self.A_slider.setValue(Default_A_Value)

        # self.A_slider.setTickInterval(tick_interval)
        # self.A_slider.setTickPosition(QSlider.TicksBelow)
        
        # # Create a label widget for displaying phase value
        # self.A_label = QLabel('1', self)
        # layout.addWidget(self.A_label)

        # # Add the phase slider to the layout
        # layout.addWidget(self.A_slider)


        # # B
        # # Create a phase slider and set its range
        # self.B_slider = QSlider(Qt.Horizontal)
        # self.B_slider.setRange(Min_B_Val, Max_B_Val)
        # self.B_slider.setValue(Default_B_Value)

        # self.B_slider.setTickInterval(tick_interval)
        # self.B_slider.setTickPosition(QSlider.TicksBelow)

        # # Create a label widget for displaying phase value
        # self.B_label = QLabel('1', self)
        # layout.addWidget(self.B_label)

        # # Add the phase slider to the layout
        # layout.addWidget(self.B_slider)


        # TEMPERATURE
        # Create an amplitude slider and set its range
        self.T_slider = QSlider(Qt.Horizontal)
        self.T_slider.setRange(Min_T_Val, Max_T_Val)
        self.T_slider.setValue(Default_T_Value)

        self.T_slider.setTickInterval(tick_interval)
        self.T_slider.setTickPosition(QSlider.TicksBelow)

        # Create a label widget for displaying amplitude value
        self.C_label = QLabel('1', self)
        layout.addWidget(self.C_label)

        # Add the amplitude slider to the layout
        layout.addWidget(self.T_slider)



        # Connect the amplitude slider's valueChanged signal to the update_plot function
        # self.A_slider.valueChanged.connect(lambda value: self.update_plot(value, self.B_slider.value(), self.T_slider.value()))
        # self.B_slider.valueChanged.connect(lambda value: self.update_plot(self.A_slider.value(), value, self.T_slider.value()))
        # self.T_slider.valueChanged.connect(lambda value: self.update_plot(self.A_slider.value(), self.B_slider.value(), value))
        self.T_slider.valueChanged.connect(lambda value: self.update_plot(value))



        # Initialize the plot
        # self.update_plot(Default_A_Value, Default_B_Value, Default_T_Value)
        self.update_plot(Default_T_Value)


    def update_plot(self, T):
        # A = A*A_scale_factor
        # B = B*B_scale_factor
        T = T*C_scale_factor

        # Update the labels with the current values
        # self.A_label.setText(f"A: {A:.3f}")
        # self.B_label.setText(f"B: {B:.3f}")
        self.C_label.setText(f"T: {T:.0f} K")

        # Clear the previous plot
        self.ax.clear()

        f_max=4e15
        # f_max=1e9
        f_nsteps=1000

        # Generate some example data
        f = np.linspace(0, f_max, f_nsteps)
        # y = A*f**2 + B*f + T
        B=2*h*(f**3)/(c**2*(np.exp(h*f/k_B/T)-1))
        P_plnk=np.sum(B[1:])*f_max/f_nsteps*A_S*np.pi # [W] itt nem kell szteradián 4-es szorzója, mert Lambert felület
        S=P_plnk/A_T
        
        # Plot the data
        self.ax.plot(f, B, linestyle="-",color="black")

        # Add grid to the plot
        self.ax.grid(True, linestyle='--', alpha=0.7)

        # Set labels and title
        self.ax.set_xlabel('f [Hz]')
        self.ax.set_ylabel('B [W/Hz/m^2/srad]')
        self.ax.axvline(790e12, linestyle="--",color="blue",alpha=0.5)
        self.ax.axvline(400e12, color="red", alpha=0.5, linestyle="--")
        self.ax.axvline(10e9, color="gray", alpha=0.5, linestyle="--")
        self.ax.axvline(10e9, color="gray", alpha=0.5, linestyle="--")
        # self.ax.axhline(k_B*T, color="gray", alpha=0.5, linestyle="--")
        self.ax.set_xlim([0,f_max])
        # self.ax.set_ylim([0,k_B*T*10])
        # self.ax.set_title(f'function y(A: {A:.3f}, B: {B:.3f} , C: {T:.3f} )')
        # self.ax.set_title(f"{np.sum(B[1:])*f_max/f_nsteps:.3f} W/m^2")
        self.ax.set_title(f"{S:.0f} W/m^2")

        # Redraw the canvas
        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWidget()
    window.show()
    sys.exit(app.exec_())
