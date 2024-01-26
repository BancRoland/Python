import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QSlider, QLabel
from PyQt5.QtCore import Qt
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# y = ax^2 + bx + c

Min_A_Val = -100
Min_B_Val = -100
Min_C_Val = -100

Max_A_Val = 100
Max_B_Val = 100
Max_C_Val = 100

Default_A_Value = 1
Default_B_Value = 0
Default_C_Value = 0

tick_interval = 1

A_scale_factor = 0.001
B_scale_factor = 0.01
C_scale_factor = 0.01


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Create a layout
        layout = QVBoxLayout(self)

        # Create a matplotlib figure and add it to the layout
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)


        # A
        # Create a phase slider and set its range
        self.A_slider = QSlider(Qt.Horizontal)
        self.A_slider.setRange(Min_A_Val, Max_A_Val)
        self.A_slider.setValue(Default_A_Value)

        self.A_slider.setTickInterval(tick_interval)
        self.A_slider.setTickPosition(QSlider.TicksBelow)
        
        # Create a label widget for displaying phase value
        self.A_label = QLabel('1', self)
        layout.addWidget(self.A_label)

        # Add the phase slider to the layout
        layout.addWidget(self.A_slider)


        # B
        # Create a phase slider and set its range
        self.B_slider = QSlider(Qt.Horizontal)
        self.B_slider.setRange(Min_B_Val, Max_B_Val)
        self.B_slider.setValue(Default_B_Value)

        self.B_slider.setTickInterval(tick_interval)
        self.B_slider.setTickPosition(QSlider.TicksBelow)

        # Create a label widget for displaying phase value
        self.B_label = QLabel('1', self)
        layout.addWidget(self.B_label)

        # Add the phase slider to the layout
        layout.addWidget(self.B_slider)


        # AMPLITUDE
        # Create an amplitude slider and set its range
        self.C_slider = QSlider(Qt.Horizontal)
        self.C_slider.setRange(Min_C_Val, Max_C_Val)
        self.C_slider.setValue(Default_C_Value)

        self.C_slider.setTickInterval(tick_interval)
        self.C_slider.setTickPosition(QSlider.TicksBelow)

        # Create a label widget for displaying amplitude value
        self.C_label = QLabel('1', self)
        layout.addWidget(self.C_label)

        # Add the amplitude slider to the layout
        layout.addWidget(self.C_slider)



        # Connect the amplitude slider's valueChanged signal to the update_plot function
        self.A_slider.valueChanged.connect(lambda value: self.update_plot(value, self.B_slider.value(), self.C_slider.value()))
        self.B_slider.valueChanged.connect(lambda value: self.update_plot(self.A_slider.value(), value, self.C_slider.value()))
        self.C_slider.valueChanged.connect(lambda value: self.update_plot(self.A_slider.value(), self.B_slider.value(), value))



        # Initialize the plot
        self.update_plot(Default_A_Value, Default_B_Value, Default_C_Value)

    def update_plot(self, A, B, C):
        A = A*A_scale_factor
        B = B*B_scale_factor
        C = C*C_scale_factor

        # Update the labels with the current values
        self.A_label.setText(f"A: {A:.3f}")
        self.B_label.setText(f"B: {B:.3f}")
        self.C_label.setText(f"C: {C:.3f}")

        # Clear the previous plot
        self.ax.clear()

        # Generate some example data
        x = np.linspace(-10, 10, 100)
        y = A*x**2 + B*x + C
 
        # Plot the data
        self.ax.plot(x, y, "-")

        # Add grid to the plot
        self.ax.grid(True, linestyle='--', alpha=0.7)

        # Set labels and title
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('y')
        self.ax.set_ylim([-1,1])
        self.ax.set_title(f'function y(A: {A:.3f}, B: {B:.3f} , C: {C:.3f} )')

        # Redraw the canvas
        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWidget()
    window.show()
    sys.exit(app.exec_())
