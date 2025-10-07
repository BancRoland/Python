import tkinter as tk

NUM_D=0 #display
NUM_M=0 #memory


prev_command=""

root = tk.Tk()
root.title("Simple calculator")

def update_mem_display():
    memory_text.config(text=f"{NUM_M} {prev_command}")

memory_text=tk.Label(root, text=NUM_M)
memory_text.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

e = tk.Entry(root, width=35, borderwidth=5)
e.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

def number_button_click(number):
    global NUM_D

    on_display=e.get()
    if on_display!="":   
        NUM_D=int(on_display)
    e.delete(0, tk.END)

    if NUM_D=="NULL":
        NUM_D=0

    NUM_D=NUM_D*10+number
    e.insert(0, NUM_D)
    return

def clear_click():
    global NUM_D
    NUM_D="NULL"
    e.delete(0, tk.END)
    e.insert(0, "")
    update_mem_display


def operation_wrapper(func):
    def wrapper(*args, **kwargs):
        global NUM_M, NUM_D

        on_display=e.get()
        if on_display!="":   
            NUM_D=int(on_display)

        if NUM_D != "NULL":
            do_calculation()
        func(*args, **kwargs)
        clear_click()
        update_mem_display()

    return wrapper

@operation_wrapper
def plus_click():
    global prev_command
    prev_command = "+"

@operation_wrapper
def minus_click():
    global prev_command
    prev_command = "-"

@operation_wrapper
def mul_click():
    global prev_command
    prev_command = "*"

@operation_wrapper
def divide_click():
    global prev_command
    prev_command = "/"

@operation_wrapper
def equal_click():
    global prev_command
    prev_command = ""



    

def do_calculation():
    global NUM_D, NUM_M

    if prev_command == "+":
        NUM_M = NUM_D + NUM_M
    elif prev_command == "-":
        NUM_M = NUM_M - NUM_D
    elif prev_command == "*":
        NUM_M = NUM_M * NUM_D
    elif prev_command == "/":
        NUM_M = NUM_M / NUM_D
    if prev_command == "":
        NUM_M = NUM_D




button_1 = tk.Button(root, text="1", padx=40, pady=20, command=lambda: number_button_click(1))
button_2 = tk.Button(root, text="2", padx=40, pady=20, command=lambda: number_button_click(2))
button_3 = tk.Button(root, text="3", padx=40, pady=20, command=lambda: number_button_click(3))
button_4 = tk.Button(root, text="4", padx=40, pady=20, command=lambda: number_button_click(4))
button_5 = tk.Button(root, text="5", padx=40, pady=20, command=lambda: number_button_click(5))
button_6 = tk.Button(root, text="6", padx=40, pady=20, command=lambda: number_button_click(6))
button_7 = tk.Button(root, text="7", padx=40, pady=20, command=lambda: number_button_click(7))
button_8 = tk.Button(root, text="8", padx=40, pady=20, command=lambda: number_button_click(8))
button_9 = tk.Button(root, text="9", padx=40, pady=20, command=lambda: number_button_click(9))
button_0 = tk.Button(root, text="0", padx=40, pady=20, command=lambda: number_button_click(0))

button_plus = tk.Button(root, text="+", padx=40, pady=20, command=plus_click)
button_minus = tk.Button(root, text="-", padx=40, pady=20, command=minus_click)
button_mul = tk.Button(root, text="*", padx=40, pady=20, command=mul_click)
button_divide = tk.Button(root, text="/", padx=40, pady=20, command=divide_click)

button_equal = tk.Button(root, text="=", padx=40, pady=20, command=equal_click)
button_clear = tk.Button(root, text="Clear", padx=40, pady=20, command=clear_click)


button_1.grid(row=3,column=0)
button_2.grid(row=3,column=1)
button_3.grid(row=3,column=2)

button_4.grid(row=2,column=0)
button_5.grid(row=2,column=1)
button_6.grid(row=2,column=2)

button_7.grid(row=1,column=0)
button_8.grid(row=1,column=1)
button_9.grid(row=1,column=2)

button_0.grid(row=4,column=1)


button_plus.grid(row=0, column=3)
button_minus.grid(row=1, column=3)
button_mul.grid(row=2, column=3)
button_divide.grid(row=3, column=3)

button_clear.grid(row=4, column=0, columnspan=1)
button_equal.grid(row=4, column=2, columnspan=1)


root.mainloop()