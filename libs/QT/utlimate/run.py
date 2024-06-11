import numpy as np
import os
import sys
from PySide6.QtCore import QPoint, Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (QPushButton, QApplication, QHBoxLayout, QGridLayout, QColorDialog,
                               QDialog, QSlider, QCheckBox, QLabel, QTabWidget, QWidget, QVBoxLayout, QFileDialog)

import matplotlib
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

filePath =""
folderPath =""
Amplitude = 1    # [] amplitude
frq = 5        # [Hz]
n_avg = 16
fc = 100         # [Hz]
fs = 500    # [Hz]
mycolor="#000000"

abs_val = False

def fun(Amplitude, frq):
    N=1000
    t=np.arange(N)/N
    return(Amplitude*np.sin(2*np.pi*frq*t))


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

        if abs_val:
            ax.plot(t,np.abs(data),color=mycolor)
            ax.set_ylim(ymin=-1.2, ymax=1.2)
            # ax.plot(t,10*np.log10(calculated),"--",color=mycolor)
            # ax.axhline(Amplitude, linestyle="--", alpha=0.5, color="gray")
            ax.set_ylabel("Amplitude []")

        else:
            ax.plot(t,data)
            # ax.plot(t,calculated,"--")
            ax.set_ylim(ymin=-1.2, ymax=1.2)
            ax.set_ylabel("Amplitude []")

        ax.set_title("Spectral Power Density of signal")
        ax.set_xlabel("time [sec]")
        ax.grid(True)
        ax.axhline(Amplitude, linestyle="--", alpha=0.5, color="C0")
        # ax.axvline(ang_dist, linestyle="--", alpha=0.5, color="gray")
        # ax.axvline(0, linestyle="--", alpha=0.5, color="gray")
        # ax.axvline(1.22*lmbda/diameter*180/np.pi, linestyle="--", alpha=0.5, color="red")
        
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
        global Amplitude, frq, n_avg

        function = fun(Amplitude, frq)
        t=np.arange(len(function))/len(function)
        
        self.plot_widget.plot(t,function)

class PlotWindow1(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Matplotlib Plot Example")
        
        layout = QVBoxLayout()
        
        self.plot_widget = MatplotlibWidget()
        layout.addWidget(self.plot_widget)
        
        self.setLayout(layout)
        self.plot_data()
        
    def plot_data(self):
        global Amplitude, frq, n_avg

        function = fun(Amplitude, frq)
        t=np.arange(len(function))/len(function)
        
        self.plot_widget.plot(t,np.abs(function))


class Form(QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.setMinimumWidth(640)
        self.setMinimumHeight(480)

        self.plot_window = PlotWindow()
        self.plot_window1 = PlotWindow1()
        mLeftPanel = QTabWidget()
        mLeftPanel.addTab(self.plot_window, 'Plot Panel')
        mLeftPanel.addTab(self.plot_window1, 'Plot Panel1')

        # Amp
        self.mTxt_A = QLabel("Amp:", self)
        self.mSldr_A = QSlider(Qt.Orientation.Horizontal)
        self.mSldr_A.setPageStep(1)
        self.mSldr_A.setRange(0,10)
        self.mSldr_A.setValue(1)
        self.mTxt_A.setText(f"Amplitude = {Amplitude} dB")
        
        # frequency
        self.mTxt_B = QLabel("frequency:", self)
        self.mSldr_B = QSlider(Qt.Orientation.Horizontal)
        self.mSldr_B.setPageStep(1)
        self.mSldr_B.setRange(0, 10)
        self.mSldr_B.setValue(5)
        self.mTxt_B.setText(f"frequency = {frq} Hz")

        # Initialize the QCheckBox
        self.mTxt_Ac = QLabel("Logaritmic scale", self)
        self.mChk_Ac = QCheckBox("Enable", self)
        self.mChk_Ac.setChecked(False)

        # Color selection
        self.mTxt_Acol = QLabel("Color Selection", self)
        self.mColor_Acol = QPushButton("Select Color", self)
        self.mColor_Acol.clicked.connect(self.openColorDialog)

        # Export button
        self.mTxt_Ab = QLabel("Button", self)
        self.mButton_Ab = QPushButton("Button_1", self)
        # self.mExport_Btn.clicked.connect(self.exportParameters)

        # File browsing button
        self.mTxt_File = QLabel("Select a file:\n", self)
        self.mBtn_File = QPushButton("Browse File", self)
        self.mBtn_File.clicked.connect(self.browse_file)

        # Folder browsing button
        self.mTxt_Folder = QLabel("Select a folder:\n", self)
        self.mBtn_Folder = QPushButton("Browse Folder", self)
        self.mBtn_Folder.clicked.connect(self.browse_folder)


        mRightPanelLyt = QGridLayout()
        mRightPanelLyt.addWidget(self.mTxt_A, 0, 0)
        mRightPanelLyt.addWidget(self.mSldr_A, 1, 0)
        mRightPanelLyt.addWidget(self.mTxt_B, 2, 0)
        mRightPanelLyt.addWidget(self.mSldr_B, 3, 0)
        mRightPanelLyt.addWidget(self.mTxt_Ac, 4, 0)
        mRightPanelLyt.addWidget(self.mChk_Ac, 4, 1)
        mRightPanelLyt.addWidget(self.mTxt_Acol, 5, 0)
        mRightPanelLyt.addWidget(self.mColor_Acol, 5, 1)
        mRightPanelLyt.addWidget(self.mTxt_Ab, 6, 0)
        mRightPanelLyt.addWidget(self.mButton_Ab, 6, 1)
        mRightPanelLyt.addWidget(self.mTxt_File, 7, 0)
        mRightPanelLyt.addWidget(self.mBtn_File, 7, 1)
        mRightPanelLyt.addWidget(self.mTxt_Folder, 8, 0)
        mRightPanelLyt.addWidget(self.mBtn_Folder, 8, 1)

        mRightPanel = QWidget()
        mRightPanel.setLayout(mRightPanelLyt)

        mMainLayout = QHBoxLayout()
        mMainLayout.addWidget(mLeftPanel)
        mMainLayout.addWidget(mRightPanel)
        mMainLayout.setStretchFactor(mLeftPanel, 2)
        mMainLayout.setStretchFactor(mRightPanel, 1)

        self.setLayout(mMainLayout)

        # connect sliders to update methods
        self.mSldr_A.valueChanged.connect(self.mUpdate__NPD_dBW)
        self.mSldr_B.valueChanged.connect(self.mUpdate__f_simb)
        self.mChk_Ac.stateChanged.connect(self.mUpdate__logscale)
        self.mButton_Ab.clicked.connect(self.mUpdate__button)


    def mUpdate__NPD_dBW(self):
        global Amplitude, frq

        Amplitude = self.mSldr_A.value()/10
        self.plot_window.plot_data()
        sx = f"NPD_dBW = {Amplitude} dB"
        self.mTxt_A.setText(sx)
        

    def mUpdate__f_simb(self):
        global Amplitude, frq
        frq = self.mSldr_B.value()
        self.plot_window.plot_data()
        sx = f"f_simb = {frq} Hz"
        self.mTxt_B.setText(sx)

    def mUpdate__logscale(self, state):
        global abs_val
        abs_val = state
        self.plot_window.plot_data()

    def mUpdate__color(self, state):
        global abs_val
        abs_val = state
        self.plot_window.plot_data()

    def openColorDialog(self):
        global mycolor
        color = QColorDialog.getColor()
        if color.isValid():
            print(f"Selected color: {color.name()}")
            mycolor=color.name()
            self.plot_window.plot_data()

    def mUpdate__button(self,state):
        print(filePath)

    def browse_file(self):
        global filePath
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*);;Text Files (*.txt)", options=options)
        if filePath:
            self.mTxt_File.setText(f"Selected file:\n {filePath}")

    def browse_folder(self):
        global folderPath
        options = QFileDialog.Options()
        folderPath = QFileDialog.getExistingDirectory(self, "Select Folder", "", options=options)
        if folderPath:
            self.mTxt_Folder.setText(f"Selected folder:\n {folderPath}")
            


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mForm = Form()
    mForm.show()
    sys.exit(app.exec())
