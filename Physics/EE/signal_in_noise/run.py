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

sys.path.append('/home/roland/Desktop/Python/DSP')
import dsp

f_simb = 10
fc = 100         # [Hz]
fs = 1000    # [Hz]
NPD_dBW = -40    # [dBW] [W/Hz] Noise Power Density 
Signalpower = 20   # [dB]
T = 5          # [sec]
n_avg = 1

def fun(NPD_dBW, f_simb):
    if f_simb==0:
        baseband_signal = np.ones(fs*T)
    else:
        size=int(np.ceil(T*f_simb))
        baseband_signal = 2*np.random.randint(2, size=size)-np.ones(size)

    # print(baseband_signal)

    n_samp0 = fs*T  # [samps]

    # sig = np.sqrt(10**(Signalpower/10))*dsp.sines(fc,fs,n_samp0)
    sig=dsp.modulate_harmronic(fc,fs,f_simb,baseband_signal)

    n_samp = len(sig)
    t=np.arange(n_samp)/fs

    NPD = 10**(NPD_dBW/10)     # [W/Hz] Noise Power Density 
    noise = np.sqrt(fs*NPD)*dsp.agwn(np.zeros(n_samp),1)
    noisy_signal=(sig+noise)
    spectrum = (np.fft.fft(noisy_signal)/np.sqrt(len(noisy_signal)))
    
    return spectrum


def fun2(NPD_dBW, f_simb, n_avg):
    if n_avg == 0:
        spectrum=np.abs(fun(NPD_dBW, f_simb))**2/fs
        return spectrum
    else:
        for i in range(n_avg):
            if i == 0:
                spectrum=np.abs(fun(NPD_dBW, f_simb))**2/fs
            else:
                spectrum=spectrum+np.abs(fun(NPD_dBW, f_simb))**2/fs
        
        return spectrum/n_avg





# c=3e8           # [m/sec]
# frequency = 500_000   # [Hz]
# lmbda=c/frequency
# diameter = 1    # [m]
# n_points = 1000
# ang_dist = 45   # [deg]

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
        ax.set_xlabel("frequency [Hz]")
        ax.set_ylabel("spectral power density [W/Hz]")
        ax.grid(True)
        # ax.set_ylim(ymin=0)
        ax.axhline(NPD_dBW, linestyle="--", alpha=0.5, color="gray")
        ax.axvline(fc, linestyle="--", alpha=0.5, color="C0")
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
        global NPD_dBW, f_simb, n_avg

        spectrum = fun2(NPD_dBW, f_simb, n_avg)
        x=np.arange(len(spectrum))/len(spectrum)*fs

        self.plot_widget.plot(x,10*np.log10(np.abs(spectrum)))


class Form(QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.setMinimumWidth(640)
        self.setMinimumHeight(480)

        self.plot_window = PlotWindow()
        
        mLeftPanel = QTabWidget()
        mLeftPanel.addTab(self.plot_window, 'Plot Panel')

        # NPD
        self.mTxt_A = QLabel("NPD_dBW:", self)
        self.mSldr_A = QSlider(Qt.Orientation.Horizontal)
        self.mSldr_A.setPageStep(1)
        self.mSldr_A.setRange(-5,0)
        self.mSldr_A.setValue(0)
        
        # f_simbol
        self.mTxt_B = QLabel("f_simb:", self)
        self.mSldr_B = QSlider(Qt.Orientation.Horizontal)
        self.mSldr_B.setPageStep(1)
        self.mSldr_B.setRange(0, 10)
        self.mSldr_B.setValue(0)

        # average number
        self.mTxt_C = QLabel("n_avg:", self)
        self.mSldr_C = QSlider(Qt.Orientation.Horizontal)
        self.mSldr_C.setPageStep(1)
        self.mSldr_C.setRange(0, 5)
        self.mSldr_C.setValue(1)

        # f_center
        self.mTxt_D = QLabel("f_center:", self)
        self.mSldr_D = QSlider(Qt.Orientation.Horizontal)
        self.mSldr_D.setPageStep(1)
        self.mSldr_D.setRange(0, 10)
        self.mSldr_D.setValue(1)

        # f_samp
        self.mTxt_E = QLabel("f_samp:", self)
        self.mSldr_E = QSlider(Qt.Orientation.Horizontal)
        self.mSldr_E.setPageStep(1)
        self.mSldr_E.setRange(1, 10)
        self.mSldr_E.setValue(1)

        # Time
        self.mTxt_F = QLabel("T:", self)
        self.mSldr_F = QSlider(Qt.Orientation.Horizontal)
        self.mSldr_F.setPageStep(1)
        self.mSldr_F.setRange(1, 10)
        self.mSldr_F.setValue(1)



        mRightPanelLyt = QGridLayout()
        mRightPanelLyt.addWidget(self.mTxt_A, 0, 0)
        mRightPanelLyt.addWidget(self.mSldr_A, 1, 0)
        mRightPanelLyt.addWidget(self.mTxt_B, 2, 0)
        mRightPanelLyt.addWidget(self.mSldr_B, 3, 0)
        mRightPanelLyt.addWidget(self.mTxt_C, 4, 0)
        mRightPanelLyt.addWidget(self.mSldr_C, 5, 0)
        mRightPanelLyt.addWidget(self.mTxt_D, 6, 0)
        mRightPanelLyt.addWidget(self.mSldr_D, 7, 0)
        mRightPanelLyt.addWidget(self.mTxt_E, 8, 0)
        mRightPanelLyt.addWidget(self.mSldr_E, 9, 0)
        mRightPanelLyt.addWidget(self.mTxt_F, 10, 0)
        mRightPanelLyt.addWidget(self.mSldr_F, 11, 0)

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
        self.mSldr_C.valueChanged.connect(self.mUpdate__n_avg)
        self.mSldr_D.valueChanged.connect(self.mUpdate__fc)
        self.mSldr_E.valueChanged.connect(self.mUpdate__fs)
        self.mSldr_F.valueChanged.connect(self.mUpdate__T)


    def mUpdate__NPD_dBW(self):
        # global frequency, diameter, ang_dist, lmbda
        global NPD_dBW, f_simb

        NPD_dBW = self.mSldr_A.value()*10
        # lmbda=c/frequency
        # diameter = self.mSldr_B.value()/10
        # ang_dist = self.mSldr_C.value()
        self.plot_window.plot_data()
        sx = f"NPD_dBW = {NPD_dBW} dB"
        self.mTxt_A.setText(sx)
        

    def mUpdate__f_simb(self):
        global NPD_dBW, f_simb
        f_simb = self.mSldr_B.value()*10
        self.plot_window.plot_data()
        sx = f"f_simb = {f_simb} Hz"
        self.mTxt_B.setText(sx)

    def mUpdate__n_avg(self):
        global NPD_dBW, f_simb, n_avg
        n_avg = 4**self.mSldr_C.value()
        self.plot_window.plot_data()
        sx = f"n_avg = {n_avg}"
        self.mTxt_C.setText(sx)

    def mUpdate__fc(self):
        global fc
        fc = fs/10*self.mSldr_D.value()
        self.plot_window.plot_data()
        sx = f"fc = {fc}"
        self.mTxt_D.setText(sx)

    def mUpdate__fs(self):
        global fs, fc
        fs = 100*self.mSldr_E.value()
        fc = fs/10*self.mSldr_D.value()
        self.plot_window.plot_data()
        sx = f"fs = {fs}"
        self.mTxt_E.setText(sx)
        sx = f"fc = {fc}"
        self.mTxt_D.setText(sx)

    def mUpdate__T(self):
        global T
        T = self.mSldr_F.value()
        self.plot_window.plot_data()
        sx = f"T = {T}"
        self.mTxt_F.setText(sx)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mForm = Form()
    mForm.show()
    sys.exit(app.exec())
