import numpy as np
import os
import sys
from PySide6.QtCore import QPoint, Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (QPushButton, QApplication, QHBoxLayout, QGridLayout,
                               QDialog, QSlider, QLabel, QTabWidget, QWidget, QVBoxLayout)

import matplotlib
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

multiplier = 1
Amplitude = 1
n_points = 1000

class MatplotlibWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Create a FigureCanvas object
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        
    def plot(self, t, data):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        # Use matplotlib.pyplot to create the plot
        ax.plot(t,data)
        ax.set_xlabel("time[sec]")
        ax.grid(True)
        
        self.canvas.draw()

class PlotWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Matplotlib Plot Example")
        
        layout = QVBoxLayout()
        
        self.plot_widget = MatplotlibWidget()
        layout.addWidget(self.plot_widget)
        
        self.setLayout(layout)
        self.plot_data(Amplitude,multiplier)
        
    def plot_data(self,Amplitude,frequency):
        t = np.arange(n_points)/n_points
        data = Amplitude*np.sin(frequency*t*np.pi*2)
        self.plot_widget.plot(t,data)

class Form(QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.setMinimumWidth(320)
        self.setMinimumHeight(240)

        self.plot_window = PlotWindow()
        
        mLeftPanel = QTabWidget()
        mLeftPanel.addTab(self.plot_window, 'Plot Panel')

        # azimuth slider
        self.mTxt_A = QLabel("azim:", self)
        self.mSldr_A = QSlider(Qt.Orientation.Horizontal)
        self.mSldr_A.setPageStep(1)
        self.mSldr_A.setRange(1, 10)
        self.mSldr_A.setValue(1)
        
        # elevation, upper slider
        self.mTxt_B = QLabel("elevu:", self)
        self.mSldr_B = QSlider(Qt.Orientation.Horizontal)
        self.mSldr_B.setPageStep(1)
        self.mSldr_B.setRange(0, 10)
        self.mSldr_B.setValue(30)

        mRightPanelLyt = QGridLayout()
        mRightPanelLyt.addWidget(self.mTxt_A, 0, 0)
        mRightPanelLyt.addWidget(self.mSldr_A, 1, 0)
        mRightPanelLyt.addWidget(self.mTxt_B, 2, 0)
        mRightPanelLyt.addWidget(self.mSldr_B, 3, 0)

        mRightPanel = QWidget()
        mRightPanel.setLayout(mRightPanelLyt)

        mMainLayout = QHBoxLayout()
        mMainLayout.addWidget(mLeftPanel)
        mMainLayout.addWidget(mRightPanel)
        mMainLayout.setStretchFactor(mLeftPanel, 2)
        mMainLayout.setStretchFactor(mRightPanel, 1)

        self.setLayout(mMainLayout)

        # connect sliders to update methods
        self.mSldr_A.valueChanged.connect(self.mUpdate_A)
        self.mSldr_B.valueChanged.connect(self.mUpdate_B)

    def mUpdate_A(self):
        Amplitude = self.mSldr_B.value()
        frequency = self.mSldr_A.value()
        self.plot_window.plot_data(Amplitude,frequency)
        sx = f"azimut={frequency} Hz"
        self.mTxt_A.setText(sx)

    def mUpdate_B(self):
        Amplitude = self.mSldr_B.value()
        frequency = self.mSldr_A.value()
        self.plot_window.plot_data(Amplitude,frequency)
        sx = f"Amplitude={Amplitude}"
        self.mTxt_B.setText(sx)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mForm = Form()
    mForm.show()
    sys.exit(app.exec())
