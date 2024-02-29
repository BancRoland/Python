import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QSlider, QLabel
from PyQt5.QtCore import Qt
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

MaxPhaseVal = 100
MaxFrqVal   = 100
MaxAmpVal   = 100

DefaultPhaseValue = 0
DefaultAmpValue = 25
DefaultFrqValue = 10

tick_interval = 1

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Create a layout
        layout = QVBoxLayout(self)

        # Create a matplotlib figure and add it to the layout
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)


        # PHASE
        # Create a phase slider and set its range
        self.phase_slider = QSlider(Qt.Horizontal)
        self.phase_slider.setRange(0, MaxPhaseVal)
        self.phase_slider.setValue(DefaultPhaseValue)

        self.phase_slider.setTickInterval(tick_interval)
        self.phase_slider.setTickPosition(QSlider.TicksBelow)
        
        # Create a label widget for displaying phase value
        self.phase_label = QLabel('0', self)
        layout.addWidget(self.phase_label)

        # Add the phase slider to the layout
        layout.addWidget(self.phase_slider)


        # FREQUENCY
        # Create a phase slider and set its range
        self.frq_slider = QSlider(Qt.Horizontal)
        self.frq_slider.setRange(0, MaxFrqVal)
        self.frq_slider.setValue(DefaultFrqValue)

        self.frq_slider.setTickInterval(tick_interval)
        self.frq_slider.setTickPosition(QSlider.TicksBelow)

        # Create a label widget for displaying phase value
        self.frq_label = QLabel('1', self)
        layout.addWidget(self.frq_label)

        # Add the phase slider to the layout
        layout.addWidget(self.frq_slider)


        # AMPLITUDE
        # Create an amplitude slider and set its range
        self.amplitude_slider = QSlider(Qt.Horizontal)
        self.amplitude_slider.setRange(0, MaxAmpVal)
        self.amplitude_slider.setValue(DefaultAmpValue)

        self.amplitude_slider.setTickInterval(tick_interval)
        self.amplitude_slider.setTickPosition(QSlider.TicksBelow)

        # Create a label widget for displaying amplitude value
        self.amplitude_label = QLabel('0.25', self)
        layout.addWidget(self.amplitude_label)

        # Add the amplitude slider to the layout
        layout.addWidget(self.amplitude_slider)



        # Connect the amplitude slider's valueChanged signal to the update_plot function
        self.amplitude_slider.valueChanged.connect(lambda value: self.update_plot(self.phase_slider.value(), value, self.frq_slider.value()))
        self.frq_slider.valueChanged.connect(lambda value: self.update_plot(self.phase_slider.value(),self.amplitude_slider.value(), value))
        self.phase_slider.valueChanged.connect(lambda value: self.update_plot(value, self.amplitude_slider.value(), self.frq_slider.value()))


        # Initialize the plot
        self.update_plot(DefaultPhaseValue, DefaultAmpValue, DefaultFrqValue)

    def update_plot(self, phase_value, amplitude_value, frq_value):
        phase_value = phase_value / MaxPhaseVal * 2 * np.pi
        amplitude_value = amplitude_value / MaxPhaseVal
        frq_value = frq_value / MaxPhaseVal * 10

        # Update the labels with the current values
        self.phase_label.setText(f"Phase: {phase_value / 2 / np.pi * 360:.1f}°")
        self.amplitude_label.setText(f"Amplitude: {amplitude_value:.2f} m")
        self.frq_label.setText(f"Frequency: {frq_value:.2f} Hz")

        # Clear the previous plot
        self.ax.clear()

        # Generate some example data
        x = np.linspace(0, 1, 100)
        y = amplitude_value * np.sin(frq_value*2 * np.pi*x + phase_value)

        # Plot the data
        self.ax.plot(x, y, "-")

        # Add grid to the plot
        self.ax.grid(True, linestyle='--', alpha=0.7)

        # Set labels and title
        self.ax.set_xlabel('time [sec]')
        self.ax.set_ylabel('Amplitude [m]')
        self.ax.set_ylim([-1,1])
        self.ax.set_title(f'Sine Wave (Phase: {phase_value / 2 / np.pi * 360:.1f}°, Amplitude: {amplitude_value:.2f} m, Frequency: {frq_value:.2f} Hz)')

        # Redraw the canvas
        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWidget()
    window.show()
    sys.exit(app.exec_())
