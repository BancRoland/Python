import tkinter as tk

root = tk.Tk()

e = tk.Entry(root, width=50)
e.pack()
e.insert(0,"Enter your name: ")

def myClick():
    myLable=tk.Label(root, text=f"Your name is {e.get()}")
    myLable.pack()

# myButton = tk.Button(root, text="Click Me!", state = "disabled")
myButton = tk.Button(root, text="Enter your name!", command=myClick)
myButton.pack()

root.mainloop()