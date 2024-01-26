import numpy as np

Sliders=np.array(["One","Two","Three"])
MaxVals=np.array([1,2,3])
DefVals = np.array([0.4,0.5,0.6])
TickVals = np.array([1,1,1])

MaxPhaseVal = 100
DefaultPhaseValue = 0
DefaultAmpValue = 25
DefaultFrqValue = 10
tick_interval = 1


print('''import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QSlider, QLabel
from PyQt5.QtCore import Qt
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas''' )

for i in range(len(Sliders)):
    print(f"Max_{Sliders[i]}_Val = {MaxVals[i]}")
    print(f"Def_{Sliders[i]}_Val = {DefVals[i]}")
    print(f"Tick_{Sliders[i]}_Val = {TickVals[i]}")

print('''class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Create a layout
        layout = QVBoxLayout(self)

        # Create a matplotlib figure and add it to the layout
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)''')


for i in range(len(Sliders)):
    print(f'''        # {Sliders[i]}
        # Create a phase slider and set its range
        self.{Sliders[i]}_slider = QSlider(Qt.Horizontal)
        self.{Sliders[i]}_slider.setRange(0, {MaxVals[i]})
        self.{Sliders[i]}_slider.setValue({DefVals[i]})

        self.{Sliders[i]}_slider.setTickInterval({TickVals[i]})
        self.{Sliders[i]}_slider.setTickPosition(QSlider.TicksBelow)
        
        # Create a label widget for displaying {Sliders[i]} value
        self.{Sliders[i]}_label = QLabel('0', self)
        layout.addWidget(self.{Sliders[i]}_label)

        # Add the {Sliders[i]} slider to the layout
        layout.addWidget(self.{Sliders[i]}_slider)''')
    

print(" # Connect the slider's valueChanged signal to the update_plot function")
for i in range(len(Sliders)):
    print(f'''self.{Sliders[i]}_slider.valueChanged.connect(lambda value: self.update_plot(''')
    for j in range(len(Sliders)):
        if i == j:
            print("value",end="")
        else:
            print(f"self.{Sliders[j]}_slider.value(),")
        print(")")

print("self.update_plot(",end="")
for i in range(len(Sliders)):
    print(f"Def_{Sliders[i]}_Val,",end="")
print(")")

print("def update_plot(self, ",end="")
for i in range(len(Sliders)):
    print(f"{Sliders[i]}_Val,",end="")
print("):")

for i in range(len(Sliders)):
    print(f"{Sliders[i]}_Val = {Sliders[i]}_Val")


for i in range(len(Sliders)):

    print(f"self.{Sliders[i]}_label.setText(f\"Amplitude: m\")")


