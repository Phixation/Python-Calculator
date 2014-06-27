#-------------------------------------------------------------------------------
# Author:      Phix
# Created:     20-06-2014
# Website:     http://www.phixation.net
#-------------------------------------------------------------------------------

from tkinter import *
from tkinter import ttk

root = Tk()
root.wm_title("Phixation Calculator")

# Create main app window by specifying resolution and x and y coordinates.
frameWidth = 420
frameHeight = 400
posX = (root.winfo_screenwidth() - frameWidth) / 2      # Center on screen x position
posY = (root.winfo_screenheight() - frameHeight) / 2    # Center on screen y position
root.geometry('%sx%s+%s+%s' % (frameWidth, frameHeight, int(posX), int(posY)))

class Calculator:

    __activeOperand = 0
    __inputs = []
    __mathFunctions = ["+","-","*", "/", "%"]
    __buttonFont = ("Arial", 16, "normal")
    __textFont = ("Verdana", 12, "normal")
    __activeValue = ""                           # Indicates the current value of the number display.
    __activeFunction = None

    def __init__(self, root):
        # Lets build the interface here.
        # Lets start with the main frame.
        mainframe = Frame(root)
        mainframe.grid(row=0, column=0, sticky=N+E+S+W)
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        # Lets start with the number display.
        self.__activeValue = StringVar()
        label = Entry(mainframe, textvariable=self.__activeValue, width=30, font=self.__textFont)
        label.grid(row=0, column=0, columnspan=2)
        label.focus()

        # The second row of our layout should contain the clear buttons.
        clearFrame = Frame(mainframe, pady=10)
        buts = []
        commands = ["back","clear","clearEntry"]
        buts.append(Button(clearFrame, text="←", width=2, height=1, padx=5, font=self.__buttonFont))    # Backspace
        buts.append(Button(clearFrame, text="CE", width=2, height=1, padx=5, font=self.__buttonFont))   # Backspace
        buts.append(Button(clearFrame, text="C", width=2, height=1, padx=5, font=self.__buttonFont))    # Backspace
        for i in range(0, len(buts)):
            buts[i].grid(row=0, column=i)
            eval("buts[i].bind('<Button-1>', self." + commands[i] + ")")

        # Now the numpad.
        numpadFrame = Frame(mainframe, padx=10, pady=10)
        colcount = 0
        rowcount = 0
        colspanner = 1
        for i in range(0,10):
            button = Button(numpadFrame, text=str(i), font=self.__buttonFont, width=3)
            button.bind("<Button-1>", self.inputNumber)
            if (i % 3 == 0) and i > 0:
                rowcount += 1
                colcount = 0
            if rowcount == 3:
                colspanner = 2
            button.grid(row=rowcount, column=colcount, columnspan=colspanner)
            colcount += 1
        button = Button(numpadFrame, text=",", font=self.__buttonFont, width=3)
        button.bind("<Button-1>", self.inputNumber)
        button.grid(row=rowcount, column=2)

        # Next up are the math function buttons like addition and subtraction.
        functionFrame = Frame(mainframe, padx=10, pady=10)
        colcount = 0
        rowcount = 0
        for i in range(0, len(self.__mathFunctions)):
            button = Button(functionFrame, text=self.__mathFunctions[i], font=self.__buttonFont, width=3)
            button.bind("<Button-1>", self.inputFunction)
            if(i % 2 == 0) and i > 0:
                rowcount += 1
                colcount = 0
            button.grid(row=rowcount, column=colcount)
            colcount += 1

        # Now lets add the button frames to the application root.
        clearFrame.grid(row=1, column=0, columnspan=2)
        numpadFrame.grid(row=2, column=0, sticky=W)
        functionFrame.grid(row=2, column=1, sticky=E)

        mainframe.rowconfigure(0, weight=1)
        mainframe.columnconfigure(0, weight=1)

    def inputNumber(self, event):
        # If previous input was a math function, clear the number display to start the input of another operand.
        # Before clearing store the current value in the __inputs list.
        # Also store the math function in the inputs list as the next item.
        # Lastly clear the __activeFunction.
        if not self.__activeFunction == None:
            self.__inputs.append(self.__activeValue.get())  # Store current input
            self.__inputs.append(self.__activeFunction)     # Store math function/operator
            self.__activeValue.set("")                      # Clear number input
            self.__activeFunction = None                    # Set function to none
        # Get the value of the number button text and add it to the current display value.
        # Prevent adding a leading zero.
        if not (self.__activeValue.get() == "" and event.widget["text"] == "0"):
            # Prevent adding more then 1 comma.
            if not ("," in self.__activeValue.get() and event.widget["text"] == ","):
                self.__activeValue.set(self.__activeValue.get() + event.widget["text"])

    def inputFunction(self, event):
        self.__activeFunction = event.widget["text"]

    def back(self, event):
        # Only backspace if number display is not empty.
        if not self.__activeValue.get() == "":
            self.__activeValue.set(self.__activeValue.get()[0:-1])

    def clear(self, event):
        self.__inputs = []
        self.__activeValue.set("")
        self.__activeFunction = None

    def clearEntry(self, event):
        self.__activeValue.set("")

app = Calculator(root)

root.mainloop()