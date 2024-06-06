import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QSlider, QLabel
from PyQt5.QtCore import Qt
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
sys.path.append('/home/roland/Desktop/Python/DSP')
import dsp

fc = 100         # [Hz]
fs = 1000    # [Hz]
NPD_dBW = -40    # [dBW] [W/Hz] Noise Power Density 
Signalpower = 20   # [dB]
T = 10          # [sec]
n_samp0 = fs*T  # [samps]
# f_simb = 50
# baseband_signal=[1,-1,1,-1,0,1]
# baseband_signal = 2*np.random.randint(2, size=N)-np.ones(N)
# baseband_signal = np.random.randint(2, size=int(np.ceil(T*f_simb)))


def fun(NPD_dBW, f_simb):
    size=int(np.ceil(T*f_simb))
    baseband_signal = 2*np.random.randint(2, size=size)-np.ones(int(np.ceil(T*f_simb)))

    # print(baseband_signal)

    # sig = np.sqrt(10**(Signalpower/10))*dsp.sines(fc,fs,n_samp0)
    sig=dsp.modulate_harmronic(fc,fs,f_simb,baseband_signal)

    n_samp = len(sig)
    t=np.arange(n_samp)/fs

    NPD = 10**(NPD_dBW/10)     # [W/Hz] Noise Power Density 
    noise = np.sqrt(fs*NPD)*dsp.agwn(np.zeros(n_samp),1)
    noisy_signal=(sig+noise)
    spectrum = np.fft.fft(noisy_signal)/np.sqrt(fs*T)
    
    return spectrum


def fun2(NPD_dBW, f_simb, N=10):
    for i in range(N):
        if i == 0:
            spectrum=np.abs(fun(NPD_dBW, f_simb))**2
        else:
            spectrum=spectrum+np.abs(fun(NPD_dBW, f_simb))**2
    
    return spectrum/N





# T=5778
# k_B=1.380649E-23 #[J/K] Boltzmann állandó
# R_S=696_340_000 #[m] földtávolság
# R_T=150E9 #[m] földtávolság

# A_S=4*R_S**2*np.pi
# A_T=4*R_T**2*np.pi

# c=3E8 #[m/s] speed of light
# h=6.62607015E-34 #[J/Hz]
# sigma=5.67E-8   #[W/m^2/K^4]




# y = ax^2 + bx + c

Min_A_Val = -100
Min_B_Val = -100
Min__NPD_dBW__Val = -50
Min__f_simb__Val = 1

Max_A_Val = 100
Max_B_Val = 100
Max__NPD_dBW__Val = 50
Max__f_simb__Val = 100

Default_A_Value = 1
Default_B_Value = 0
Default__NPD_dBW__Value = 0
Default__f_simb__Value = 1


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
        self.NPD_dBW__slider = QSlider(Qt.Horizontal)
        self.NPD_dBW__slider.setRange(Min__NPD_dBW__Val, Max__NPD_dBW__Val)
        self.NPD_dBW__slider.setValue(Default__NPD_dBW__Value)

        self.NPD_dBW__slider.setTickInterval(tick_interval)
        self.NPD_dBW__slider.setTickPosition(QSlider.TicksBelow)

        # Create a label widget for displaying amplitude value
        self.C_label = QLabel('1', self)
        layout.addWidget(self.C_label)


        # TEMPERATURE
        # Create an amplitude slider and set its range
        self.f_simb__slider = QSlider(Qt.Horizontal)
        self.f_simb__slider.setRange(Min__f_simb__Val, Max__f_simb__Val)
        self.f_simb__slider.setValue(Default__f_simb__Value)

        self.f_simb__slider.setTickInterval(tick_interval)
        self.f_simb__slider.setTickPosition(QSlider.TicksBelow)

        # Create a label widget for displaying amplitude value
        self.f_simb_label = QLabel('2', self)
        layout.addWidget(self.f_simb_label)

        # Add the amplitude slider to the layout
        layout.addWidget(self.NPD_dBW__slider)
        layout.addWidget(self.f_simb__slider)



        # Connect the amplitude slider's valueChanged signal to the update_plot function
        # self.A_slider.valueChanged.connect(lambda value: self.update_plot(value, self.B_slider.value(), self.T_slider.value()))
        # self.B_slider.valueChanged.connect(lambda value: self.update_plot(self.A_slider.value(), value, self.T_slider.value()))
        # self.T_slider.valueChanged.connect(lambda value: self.update_plot(self.A_slider.value(), self.B_slider.value(), value))
        # self.NPD_dBW__slider.valueChanged.connect(lambda value: self.update_plot(value))
        # self.f_simb__slider.valueChanged.connect(lambda value: self.update_plot(value))

        # Connect the amplitude slider's valueChanged signal to the update_plot function
        self.NPD_dBW__slider.valueChanged.connect(lambda value: self.update_plot(value, self.f_simb__slider.value()))
        self.f_simb__slider.valueChanged.connect(lambda value: self.update_plot(self.NPD_dBW__slider.value(), value))



        # Initialize the plot
        # self.update_plot(Default_A_Value, Default_B_Value, Default_T_Value)
        self.update_plot(Default__NPD_dBW__Value,Default__f_simb__Value)


    def update_plot(self, NPD_dBW,f_simb):
        # A = A*A_scale_factor
        # B = B*B_scale_factor
        NPD_dBW = NPD_dBW*C_scale_factor

        # Update the labels with the current values
        # self.A_label.setText(f"A: {A:.3f}")
        # self.B_label.setText(f"B: {B:.3f}")
        self.C_label.setText(f"SNR: {NPD_dBW:.0f} dB")
        self.f_simb_label.setText(f"f_simb: {NPD_dBW:.0f} dB")

        # Clear the previous plot
        self.ax.clear()


        # Plot the data
        # self.ax.plot(f, B, linestyle="-",color="black")
        spectrum = fun2(NPD_dBW,f_simb)
        self.ax.plot(np.abs(spectrum), linestyle="-",color="black")


        # Add grid to the plot
        self.ax.grid(True, linestyle='--', alpha=0.7)

        # # Set labels and title
        # self.ax.set_xlabel('f [Hz]')
        # self.ax.set_ylabel('B [W/Hz/m^2/srad]')
        # self.ax.axvline(790e12, linestyle="--",color="blue",alpha=0.5)
        # self.ax.axvline(400e12, color="red", alpha=0.5, linestyle="--")
        # self.ax.axvline(10e9, color="gray", alpha=0.5, linestyle="--")
        # self.ax.axvline(10e9, color="gray", alpha=0.5, linestyle="--")
        # self.ax.axhline(k_B*T, color="gray", alpha=0.5, linestyle="--")
        # self.ax.set_xlim([0,f_max])
        # self.ax.set_ylim([0,k_B*T*10])
        # self.ax.set_title(f'function y(A: {A:.3f}, B: {B:.3f} , C: {T:.3f} )')
        # self.ax.set_title(f"{np.sum(B[1:])*f_max/f_nsteps:.3f} W/m^2")
        # self.ax.set_title(f"{S:.0f} W/m^2")

        # Redraw the canvas
        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWidget()
    window.show()
    sys.exit(app.exec_())
