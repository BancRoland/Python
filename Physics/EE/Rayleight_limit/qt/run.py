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

c=3e8           # [m/sec]
frequency = 500_000   # [Hz]
lmbda=c/frequency
diameter = 1    # [m]
n_points = 1000
ang_dist = 45   # [deg]

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
        ax.set_xlabel("angle [deg]")
        ax.set_ylabel("power [W]")
        ax.grid(True)
        ax.axvline(ang_dist, linestyle="--", alpha=0.5, color="gray")
        ax.axvline(0, linestyle="--", alpha=0.5, color="gray")
        ax.axvline(1.22*lmbda/diameter*180/np.pi, linestyle="--", alpha=0.5, color="red")
        
        self.canvas.draw()

class PlotWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Matplotlib Plot Example")
        
        layout = QVBoxLayout()
        
        self.plot_widget = MatplotlibWidget()
        layout.addWidget(self.plot_widget)
        
        self.setLayout(layout)
        self.plot_data()
        
    def plot_data(self):
        global frequency, diameter, ang_dist, lmbda

        x = 180*(np.arange(n_points)/n_points-0.5)
        k=lmbda/diameter
        # data = np.sin(x/180*np.pi*np.pi/k)/(x/180*np.pi*np.pi/k)
        data = np.sinc(x/180*np.pi/k)   # sinc() function works as sin(pi*x)/(pi*x)
        # power=data**2
        power=(np.sinc(x/180*np.pi/k))**2+(np.sinc((x-ang_dist)/180*np.pi/k))**2
        self.plot_widget.plot(x,power)

class Form(QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.setMinimumWidth(640)
        self.setMinimumHeight(480)

        self.plot_window = PlotWindow()
        
        mLeftPanel = QTabWidget()
        mLeftPanel.addTab(self.plot_window, 'Plot Panel')

        # frequency slider
        self.mTxt_A = QLabel("frequency:", self)
        self.mSldr_A = QSlider(Qt.Orientation.Horizontal)
        self.mSldr_A.setPageStep(1)
        self.mSldr_A.setRange(1,100)
        self.mSldr_A.setValue(50)
        
        # diameter, upper slider
        self.mTxt_B = QLabel("diameter:", self)
        self.mSldr_B = QSlider(Qt.Orientation.Horizontal)
        self.mSldr_B.setPageStep(1)
        self.mSldr_B.setRange(1, 100)
        self.mSldr_B.setValue(10)

        # angular distance, upper slider
        self.mTxt_C = QLabel("angular distance:", self)
        self.mSldr_C = QSlider(Qt.Orientation.Horizontal)
        self.mSldr_C.setPageStep(1)
        self.mSldr_C.setRange(0, 90)
        self.mSldr_C.setValue(45)

        mRightPanelLyt = QGridLayout()
        mRightPanelLyt.addWidget(self.mTxt_A, 0, 0)
        mRightPanelLyt.addWidget(self.mSldr_A, 1, 0)
        mRightPanelLyt.addWidget(self.mTxt_B, 2, 0)
        mRightPanelLyt.addWidget(self.mSldr_B, 3, 0)
        mRightPanelLyt.addWidget(self.mTxt_C, 4, 0)
        mRightPanelLyt.addWidget(self.mSldr_C, 5, 0)

        mRightPanel = QWidget()
        mRightPanel.setLayout(mRightPanelLyt)

        mMainLayout = QHBoxLayout()
        mMainLayout.addWidget(mLeftPanel)
        mMainLayout.addWidget(mRightPanel)
        mMainLayout.setStretchFactor(mLeftPanel, 2)
        mMainLayout.setStretchFactor(mRightPanel, 1)

        self.setLayout(mMainLayout)

        # connect sliders to update methods
        self.mSldr_A.valueChanged.connect(self.mUpdate_frequency)
        self.mSldr_B.valueChanged.connect(self.mUpdate_diameter)
        self.mSldr_C.valueChanged.connect(self.mUpdate_ang_dist)


    def mUpdate_frequency(self):
        global frequency, diameter, ang_dist, lmbda
        frequency = self.mSldr_A.value()*10_000_000
        lmbda=c/frequency
        # diameter = self.mSldr_B.value()/10
        # ang_dist = self.mSldr_C.value()
        self.plot_window.plot_data()
        sx = f"frequency = {frequency/1e6} MHz"
        self.mTxt_A.setText(sx)

    def mUpdate_diameter(self):
        global frequency, diameter, ang_dist
        # frequency = self.mSldr_A.value()*10_000_000
        diameter = self.mSldr_B.value()/10
        # ang_dist = self.mSldr_C.value()
        self.plot_window.plot_data()
        sx = f"diameter = {diameter} m"
        self.mTxt_B.setText(sx)

    def mUpdate_ang_dist(self):
        global frequency, diameter, ang_dist, lmbda
        # frequency = self.mSldr_A.value()*10_000_000
        # lmbda=c/frequency
        # diameter = self.mSldr_B.value()/10
        ang_dist = self.mSldr_C.value()
        self.plot_window.plot_data()
        sx = f"angular distance = {ang_dist} deg"
        self.mTxt_C.setText(sx)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mForm = Form()
    mForm.show()
    sys.exit(app.exec())
