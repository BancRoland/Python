import tkinter as tk

root = tk.Tk()

def myClick():
    myLable=tk.Label(root, text="Look! I clickd a Button!")
    myLable.pack()

# myButton = tk.Button(root, text="Click Me!", state = "disabled")
myButton = tk.Button(root, text="Click Me!", padx=50, pady=50, command=myClick, fg="blue", bg="red")
myButton.pack()

root.mainloop()