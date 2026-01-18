
from StatManager import StatManager
from tkinter import *
# Defining main function
class main:
    def __init__(self):
        self.root = Tk() #Makes the window
        self.root.wm_title("Window Title") #Makes the title that will appear in the top left
        self.Frame1 = Frame(self.root, width=200, height = 600)
        self.leftPanel = StatManager(self.root, self.Frame1)

    def start(self):
        self.root.mainloop() #start monitoring and updating the GUI

# Using the special variable
# __name__
if __name__=="__main__":
    root =  main()
    root.start()