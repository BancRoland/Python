import numpy as np
import matplotlib.pyplot as plt

import tkinter as tk

def start():
    print("Start button pressed")

def refresh():
    print("Refresh button pressed")

def stop():
    root.destroy()  # Close the window

# Create main window
root = tk.Tk()
root.title("Control Panel")
root.geometry("300x200")

# Create buttons
start_button = tk.Button(root, text="Start", width=15, command=start)
refresh_button = tk.Button(root, text="Refresh", width=15, command=refresh)
stop_button = tk.Button(root, text="Stop", width=15, command=stop)

# Place buttons
start_button.pack(pady=10)
refresh_button.pack(pady=10)
stop_button.pack(pady=10)

# Run the application
root.mainloop()
