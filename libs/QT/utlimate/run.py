import numpy as np
import os
import io
import sys
import folium
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (QPushButton, QApplication, 
                               QHBoxLayout, QVBoxLayout,
                               QDialog, QSlider, 
                               QCheckBox, QLabel, 
                               QTabWidget, QWidget, 
                               QColorDialog, QFileDialog, 
                               QGridLayout, QLineEdit,
                               QComboBox)
from PySide6.QtWebEngineWidgets import QWebEngineView

import matplotlib
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

filePath =""
folderPath =""
Amplitude = 1    # [] amplitude
frq = 50        # [Hz]
mycolor="#000000"
line_edit_val = 10

abs_val = False

def fun(Amplitude, frq):
    N=1000
    t=np.arange(N)/N
    return(Amplitude*np.sin(2*np.pi*frq*t))

class FloatInputWidget(QWidget):
    def __init__(self, label_text="", default_value=0.0, parent=None):
        super().__init__(parent)
        
        self.label = QLabel(label_text)
        self.line_edit = QLineEdit(str(default_value))
        
        layout = QHBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.line_edit)
        
        self.setLayout(layout)
        
    def value(self):
        try:
            return float(self.line_edit.text())
        except ValueError:
            return None

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

        else:
            ax.plot(t,data,color=mycolor)
            ax.set_ylim(ymin=-1.2, ymax=1.2)

        ax.set_title("Harmonic signal")
        ax.set_ylabel("Amplitude []")
        ax.set_xlabel("time [sec]")
        ax.grid(True)
        ax.axhline(Amplitude, linestyle="--", alpha=0.5, color=mycolor)
        
        self.canvas.draw()


    def plot2(self, data):

        self.figure.clear()
        ax = self.figure.add_subplot(111)

        f=np.arange(len(data))
        ax.plot(f,data, color=mycolor)
        ax.set_ylabel("Amplitude []")
        ax.set_xlabel("frequency [Hz]")

        ax.set_title("Harmonic signal")
        ax.grid(True)
        ax.axhline(Amplitude, linestyle="--", alpha=0.5, color=mycolor)
        
        self.canvas.draw()

class MapWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        
        self.map_view = QWebEngineView()
        layout.addWidget(self.map_view)
        
        self.setLayout(layout)
        self.create_map()
        self.display_map()
        
    def create_map(self):
        self.map = folium.Map(location=[45.5236, -122.6750], zoom_start=13)
    
    def display_map(self):
        data = io.BytesIO()
        self.map.save(data, close_file=False)
        
        self.map_view.setHtml(data.getvalue().decode())

    def add_point(self, lat, lon, popup_text):
        folium.Marker(location=[lat, lon], popup=popup_text).add_to(self.map)
        self.display_map()



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
        global Amplitude, frq

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
        global Amplitude, frq

        function = fun(Amplitude, frq)
        t=np.arange(len(function))/len(function)
        
        self.plot_widget.plot2(np.abs(np.fft.fft(function)))


class Form(QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.setMinimumWidth(640)
        self.setMinimumHeight(480)

        self.plot_window = PlotWindow()
        self.plot_window1 = PlotWindow1()
        self.map_widget = MapWidget()


        self.mLeftPanel = QTabWidget()
        self.mLeftPanel.addTab(self.plot_window, 'Plot Panel 1')
        self.mLeftPanel.addTab(self.plot_window1, 'Plot Panel 2')
        self.mLeftPanel.addTab(self.map_widget, 'Map Panel')



        # Create multiple variable panels
        self.mRightPanel1 = self.create_variable_panel_1()
        self.mRightPanel2 = self.create_variable_panel_2()

        self.mRightTabs = QTabWidget()
        self.mRightTabs.addTab(self.mRightPanel1, 'Variables 1')
        self.mRightTabs.addTab(self.mRightPanel2, 'Variables 2')

        self.mMainLayout = QHBoxLayout()
        self.mMainLayout.addWidget(self.mLeftPanel)
        self.mMainLayout.addWidget(self.mRightTabs)
        self.mMainLayout.setStretchFactor(self.mLeftPanel, 2)
        self.mMainLayout.setStretchFactor(self.mRightTabs, 1)

        self.setLayout(self.mMainLayout)

        # Timer for debouncing slider changes
        self.update_timer = QTimer(self)
        self.update_timer.setSingleShot(True)
        self.update_timer.timeout.connect(self.update_plot)

        # Connect sliders to update methods
        self.mSldr_A.valueChanged.connect(self.on_slider_value_changed)
        self.mSldr_B.valueChanged.connect(self.on_slider_value_changed)

        self.mChk_Ac.stateChanged.connect(self.mUpdate__logscale)
        self.mButton_Ab.clicked.connect(self.mUpdate__button)
        self.mLineEdit_Al.editingFinished.connect(self.mUpdate__LineEdit)

        # Add points to the map as an example
        self.map_widget.add_point(45.5236, -122.6750, "Point 1")
        self.map_widget.add_point(45.5289, -122.6801, "Point 2")


    def create_variable_panel_1(self):
        panel = QWidget()
        layout = QGridLayout()


        # Amp
        self.mTxt_A = QLabel("Amp:", self)
        self.mSldr_A = QSlider(Qt.Orientation.Horizontal)
        self.mSldr_A.setPageStep(1)
        self.mSldr_A.setRange(0,100)
        self.mSldr_A.setValue(100)
        self.mTxt_A.setText(f"Amplitude = {Amplitude} dB")
        layout.addWidget(self.mTxt_A, 0, 0)
        layout.addWidget(self.mSldr_A, 1, 0)
        
        # frequency
        self.mTxt_B = QLabel("frequency:", self)
        self.mSldr_B = QSlider(Qt.Orientation.Horizontal)
        self.mSldr_B.setPageStep(1)
        self.mSldr_B.setRange(0, 100)
        self.mSldr_B.setValue(50)
        self.mTxt_B.setText(f"frequency = {frq} Hz")
        layout.addWidget(self.mTxt_B, 2, 0)
        layout.addWidget(self.mSldr_B, 3, 0)

        # Export button
        self.mTxt_Ab = QLabel("Button", self)
        self.mButton_Ab = QPushButton("Button_1", self)
        # self.mExport_Btn.clicked.connect(self.exportParameters)
        layout.addWidget(self.mTxt_Ab, 4, 0)
        layout.addWidget(self.mButton_Ab, 4, 1)

        # Color selection
        self.mTxt_Acol = QLabel("Color Selection", self)
        self.mColor_Acol = QPushButton("Select Color", self)
        self.mColor_Acol.clicked.connect(self.openColorDialog)
        layout.addWidget(self.mTxt_Acol, 5, 0)
        layout.addWidget(self.mColor_Acol, 5, 1)

        # Line edit
        self.mTxt_Al = QLabel("LineEdit:", self)
        self.mLineEdit_Al = QLineEdit("", self)
        self.mTxt_Al.setText(f"Line Edit:")
        layout.addWidget(self.mTxt_Al, 6, 0)
        layout.addWidget(self.mLineEdit_Al, 6, 1)

        # combo_box
        self.mTxt_Addm = QLabel("menu", self)
        self.mMenu_Addm = QComboBox(self)
        # self.mExport_Btn.clicked.connect(self.exportParameters)
        self.mMenu_Addm.addItems(["Option 1", "Option 2", "Option 3"])
        self.mMenu_Addm.currentIndexChanged.connect(self.option_selected)
        layout.addWidget(self.mTxt_Addm, 7, 0)
        layout.addWidget(self.mMenu_Addm, 7, 1)
        
        panel.setLayout(layout)
        return panel

    def create_variable_panel_2(self):
        panel = QWidget()
        layout = QGridLayout()
        
        # Checkbox
        self.mTxt_Ac = QLabel("absolute value", panel)
        self.mChk_Ac = QCheckBox("Enable", panel)
        self.mChk_Ac.setChecked(False)
        layout.addWidget(self.mTxt_Ac, 1, 0)
        layout.addWidget(self.mChk_Ac, 1, 1)

        # File browsing button
        self.mTxt_File = QLabel("Select a file:", panel)
        self.mBtn_File = QPushButton("Browse File", panel)
        self.mBtn_File.clicked.connect(self.browse_file)
        layout.addWidget(self.mTxt_File, 2, 0)
        layout.addWidget(self.mBtn_File, 2, 1)

        # Folder browsing button
        self.mTxt_Folder = QLabel("Select a folder:", panel)
        self.mBtn_Folder = QPushButton("Browse Folder", panel)
        self.mBtn_Folder.clicked.connect(self.browse_folder)
        layout.addWidget(self.mTxt_Folder, 3, 0)
        layout.addWidget(self.mBtn_Folder, 3, 1)
        
        panel.setLayout(layout)
        return panel


    def mUpdate__logscale(self, state):
        global abs_val
        abs_val = state
        self.plot_window.plot_data()
        self.plot_window1.plot_data()


    def mUpdate__color(self, state):
        global abs_val
        abs_val = state
        self.plot_window.plot_data()
        self.plot_window1.plot_data()


    def openColorDialog(self):
        global mycolor
        color = QColorDialog.getColor()
        if color.isValid():
            print(f"Selected color: {color.name()}")
            mycolor=color.name()
            self.plot_window.plot_data()
            self.plot_window1.plot_data()


    def mUpdate__button(self,state):
        print(filePath)

    def mUpdate__LineEdit(self):
        global line_edit_val
        line_edit_val = self.mLineEdit_Al.text()
        print(line_edit_val)

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


    def on_slider_value_changed(self):
        self.update_timer.start(20)

    def update_plot(self):
        global Amplitude

        Amplitude = self.mSldr_A.value() / 100
        self.mTxt_A.setText(f"Amp: {Amplitude}")


        global frq

        self.mTxt_B.setText(f"frequency: {frq} Hz")
        frq = self.mSldr_B.value()

        self.plot_window.plot_data()
        self.plot_window1.plot_data()

    def option_selected(self):
        # Get the currently selected option
        selected_option = self.mMenu_Addm.currentText()
        # Update the label with the selected option
        self.mTxt_Addm.setText(f"{selected_option} selected")

            

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mForm = Form()
    mForm.show()
    sys.exit(app.exec())
