from tkinter import *
from main import *

class StartFrame:
    def __init__(self, master):
        self.master = master
        master.title("Test GUI")
        master.geometry("800x400")

        self.label = Label(master, text="Stock Tracker")
        self.label.pack()

        self.add_symbol = Button(master, text="Add Symbol", command=self.add_symbol)
        self.add_symbol.pack()

        self.greet_button = Button(master, text="Greet", command=self.greet)
        self.greet_button.pack()

        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack()

    def greet(self):
        print("Greetings!")

    def add_symbol(self, symb):
        symbols[symbol] = Symbol(symb)

root = Tk()
my_gui = StartFrame(root)
root.mainloop()
