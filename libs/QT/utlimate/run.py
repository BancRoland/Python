import numpy as np
import os
import sys
from PySide6.QtCore import QPoint, Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (QPushButton, QApplication, QHBoxLayout, QGridLayout, QColorDialog,
                               QDialog, QSlider, QCheckBox, QLabel, QTabWidget, QWidget, QVBoxLayout)


import matplotlib
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


# Get the current file's directory
current_dir = os.path.dirname(os.path.abspath(__file__))
relative_path = os.path.join(current_dir, '../../../DSP')

sys.path.append(relative_path)
# sys.path.append('/home/bancr/Desktop/Python/DSP')
import dsp

NPD_dBW = -40    # [dBW] [W/Hz] Noise Power Density 
f_simb = 50
n_avg = 16
fc = 100         # [Hz]
fs = 500    # [Hz]
# Signalpower = 20   # [dB]
T = 1          # [sec]
mycolor="#000000"

log_val = False

def fun(NPD_dBW, f_simb):
    if f_simb==0:
        baseband_signal = np.ones(fs*T)
    else:
        size=int(np.ceil(T*f_simb))
        # baseband_signal = 2*np.random.randint(2, size=size)-np.ones(size)
        # baseband_signal=dsp.get_random_bpsk(size)
        # baseband_signal=dsp.get_random_ook(size)
        # baseband_signal=dsp.get_random_qpsk(size)
        baseband_signal=dsp.get_random_npsk(size,128)
        # baseband_signal=dsp.get_random_manchester(size)

    # print(baseband_signal)

    n_samp0 = fs*T  # [samps]

    # sig = np.sqrt(10**(Signalpower/10))*dsp.sines(fc,fs,n_samp0)
    sig=dsp.modulate_harmronic(fc,fs,f_simb,baseband_signal)[:n_samp0:]

    n_samp = len(sig)
    t=np.arange(n_samp)/fs

    NPD = 10**(NPD_dBW/10)     # [W/Hz] Noise Power Density 
    noise = np.sqrt(fs*NPD)*dsp.agwn(np.zeros(n_samp),1)
    noisy_signal=(sig+noise)
    spectrum = np.fft.fft(noisy_signal)/np.sqrt(len(noisy_signal))
    
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
        if 0:
            x=(t-fc)/f_simb*np.pi
            calculated=(np.sin(x)/x)**2/f_simb+10**(NPD_dBW/10)
        else:
            calculated=np.zeros(len(t))
            for i in range(-20,20):
                x=(t-fc-i*fs)/f_simb*np.pi
                calculated=calculated+(np.sin(x)/x)**2/f_simb
            calculated+=10**(NPD_dBW/10)

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        # Use matplotlib.pyplot to create the plot

        if log_val:
            ax.plot(t,10*np.log10(data))
            ax.plot(t,10*np.log10(calculated),"--",color=mycolor)
            ax.axhline(NPD_dBW, linestyle="--", alpha=0.5, color="gray")
            ax.set_ylabel("spectral power density [dBW/Hz]")

        else:
            ax.plot(t,data)
            ax.plot(t,calculated,"--")
            ax.set_ylim(ymin=0)
            ax.set_ylabel("spectral power density [W/Hz]")

        ax.set_title("Spectral Power Density of signal")
        ax.set_xlabel("frequency [Hz]")
        ax.grid(True)
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
        
        self.plot_widget.plot(x,np.abs(spectrum))


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
        self.mSldr_A.setValue(-4)
        self.mTxt_A.setText(f"NPD_dBW = {NPD_dBW} dB")
        
        # f_simbol
        self.mTxt_B = QLabel("f_simb:", self)
        self.mSldr_B = QSlider(Qt.Orientation.Horizontal)
        self.mSldr_B.setPageStep(1)
        self.mSldr_B.setRange(0, 10)
        self.mSldr_B.setValue(5)
        self.mTxt_B.setText(f"f_simb = {f_simb} Hz")

        # Initialize the QCheckBox
        self.mTxt_Ac = QLabel("Logaritmic scale", self)
        self.mChk_Ac = QCheckBox("Enable", self)
        self.mChk_Ac.setChecked(False)

        # Color selection
        self.mTxt_As = QLabel("Color Selection", self)
        self.mColor_Ac = QPushButton("Select Color", self)
        self.mColor_Ac.clicked.connect(self.openColorDialog)

        # Color selection
        self.mTxt_As = QLabel("Color Selection", self)
        self.mColor_Ac = QPushButton("Select Color", self)
        self.mColor_Ac.clicked.connect(self.openColorDialog)

        mRightPanelLyt = QGridLayout()
        mRightPanelLyt.addWidget(self.mTxt_A, 0, 0)
        mRightPanelLyt.addWidget(self.mSldr_A, 1, 0)
        mRightPanelLyt.addWidget(self.mTxt_B, 2, 0)
        mRightPanelLyt.addWidget(self.mSldr_B, 3, 0)
        mRightPanelLyt.addWidget(self.mTxt_Ac, 4, 0)
        mRightPanelLyt.addWidget(self.mChk_Ac, 4, 1)
        mRightPanelLyt.addWidget(self.mTxt_As, 5, 0)
        mRightPanelLyt.addWidget(self.mColor_Ac, 5, 1)

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

    def mUpdate__logscale(self, state):
        global log_val
        log_val = state
        self.plot_window.plot_data()

    def mUpdate__color(self, state):
        global log_val
        log_val = state
        self.plot_window.plot_data()

    def openColorDialog(self):
        global mycolor
        color = QColorDialog.getColor()
        if color.isValid():
            print(f"Selected color: {color.name()}")
            # Here you can use the selected color to update plot or other elements
            # For example, updating the label background color:
            mycolor=color.name()
            self.plot_window.plot_data()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mForm = Form()
    mForm.show()
    sys.exit(app.exec())
