import tkinter as tk
import board
import tkinter.filedialog
import tkinter.messagebox
import sys, string, os, time, threading, subprocess 


class Onitama(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.blueIsComputer = False
        self.redIsComputer = False
        self.gameIsOver = False
        self.gameIsRunning = False

        self.control = ControlPanel(self)
        self.control.pack(anchor=tk.E)

        self.b = board.Board(self)
        self.b.pack()
    
    def startGame(self):
        if self.gameIsOver:
            print("Cannnot start: game is over")
            return
        self.control.disableSetupOptions()
        self.gameIsRunning = True
        if (self.b.turn and self.blueIsComputer) or (not self.b.turn and self.redIsComputer):
            self.makeComputerMove()

    def makeComputerMove(self):
        #use threading because otherwise, with 2 computer users, MainLoop freezes until the game has finished.
        threading.Thread(target=self.computerMovementThread).start()


    def computerMovementThread(self):
        self.b.writeGameState()
        if self.b.turn and self.blueIsComputer:
            try:
                subprocess.run(self.control.blueFilename, timeout=self.control.timeout)
            except subprocess.TimeoutExpired:
                tkinter.messagebox.showinfo(title="AI Timeout", message="Blue's AI took too long thinking of a move... Game Over.")
                return
        elif not self.b.turn and self.redIsComputer:
            try:
                subprocess.run(self.control.redFilename, timeout=self.control.timeout)
            except subprocess.TimeoutExpired:
                tkinter.messagebox.showinfo(title="AI Timeout", message="Red's AI took too long thinking of a move... Game Over.")
                return
        

        if (self.b.turn and self.blueIsComputer) or (not self.b.turn and self.redIsComputer):
            if self.control.wait.get():
                time.sleep(1)
            with open("moves.txt") as infile:
                lastline = None
                for line in infile:
                    lastline = line
            print(f"attempted computer move: {lastline}")
            datalist = lastline.split(' ')
            currLoc = list(map(int, datalist[0].split(',')))
            currLoc.reverse()
            currLoc = tuple(currLoc)
            moveTo = list(map(int, datalist[1].split(',')))
            moveTo.reverse()
            moveTo = tuple(moveTo)
            cardName = datalist[2].strip()
            self.b.makeMove(currLoc, moveTo, cardName)
            

    def resetGame(self):
        self.b.destroy()
        self.b = board.Board(self)
        self.b.pack()
        self.control.enableSetupOptions()
        self.gameIsOver = False
        self.gameIsRunning = False










class ControlPanel(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.blueFilename = None
        self.redFilename = None
        self.blueComputer = tk.IntVar()
        self.redComputer = tk.IntVar()
        self.wait = tk.IntVar()
        self.timeoutstr = tk.StringVar()
        self.timeOutChoices = ['1 sec','5 sec','10 sec','20 sec','30 sec', '1 min','Indefinite']
        self.timeoutstr.set(self.timeOutChoices[3]) # set the default option
        self.timeout = None

        self.blueLabel = tk.Label(self, text="Is Blue a Computer?")
        self.redLabel = tk.Label(self, text="Is Red a Computer?")
        self.chkBlueComp = tk.Checkbutton(self, variable=self.blueComputer, command=self.selectBlueComp)
        self.chkRedComp = tk.Checkbutton(self, variable=self.redComputer, command=self.selectRedComp)
        self.chkWait = tk.Checkbutton(self, variable=self.wait, text="Slow computer moves\nto be human visible")
        self.goButton = tk.Button(self, text="Start Game", command=self.master.startGame, bg="lime")
        self.resetButton = tk.Button(self, text="Reset Game", command=self.master.resetGame, bg="pink")
        self.timeoutLabel = tk.Label(self, text="Stop waiting for AI after:")
        self.timeOutMenu = tk.OptionMenu(self, self.timeoutstr, *self.timeOutChoices, command=self.setTimeout)

        self.blueLabel.grid(column=0, row=0)
        self.redLabel.grid(column=0, row=1)
        self.chkBlueComp.grid(column=1, row=0, sticky="W")
        self.chkRedComp.grid(column=1, row=1, sticky="W")
        self.grid_columnconfigure(1, minsize=100)
        self.timeoutLabel.grid(column=2, row=0)
        self.timeOutMenu.grid(column=2, row=1)
        self.chkWait.grid(column=3, row=0, rowspan=2, padx=(50,0))
        self.goButton.grid(column=4, row=0, rowspan=2, padx=(50,0))
        self.resetButton.grid(column=5, row=0, rowspan=2, padx=(50,0))

    def selectBlueComp(self):
        if self.blueComputer.get():
            self.blueFilename = tkinter.filedialog.askopenfilename(initialdir = "./", title = "Select AI Player for Blue", filetypes = (("executable files","*.exe"),("all files","*.*")))
            if(self.blueFilename):
                self.chkBlueComp.config(text=self.blueFilename.split('/')[-1])
                self.master.blueIsComputer = True
                self.master.b.blue1.disable()
                self.master.b.blue2.disable()
            else:
                self.blueFilename = None
                self.master.blueIsComputer = False
                self.blueComputer.set(False)
                if self.master.b.turn:
                    self.master.b.blue1.enable()
                    self.master.b.blue2.enable()
        else:
            self.chkBlueComp.config(text="")
            self.master.blueIsComputer = False
            if self.master.b.turn:
                self.master.b.blue1.enable()
                self.master.b.blue2.enable()
        
    def selectRedComp(self):
        if self.redComputer.get():
            self.redFilename = tkinter.filedialog.askopenfilename(initialdir = "./", title = "Select AI Player for Red", filetypes = (("executable files","*.exe"),("all files","*.*")))
            if(self.redFilename):
                self.chkRedComp.config(text=self.redFilename.split('/')[-1])
                self.master.redIsComputer = True
                self.master.b.red1.disable()
                self.master.b.red2.disable()
                #os.system(self.redFilename)
            else:
                self.redFilename = None
                self.master.blueIsComputer = False
                self.redComputer.set(False)
                if not self.master.b.turn:
                    self.master.b.red1.enable()
                    self.master.b.red2.enable()
        else:
            self.chkRedComp.config(text="")
            self.master.blueIsComputer = False
            if not self.master.b.turn:
                self.master.b.red1.enable()
                self.master.b.red2.enable()
    
    def enableSetupOptions(self):
        self.goButton.configure(state=tk.NORMAL)
        self.chkBlueComp.configure(state=tk.NORMAL)
        self.chkRedComp.configure(state=tk.NORMAL)

    def disableSetupOptions(self):
        self.goButton.configure(state=tk.DISABLED)
        self.chkBlueComp.configure(state=tk.DISABLED)
        self.chkRedComp.configure(state=tk.DISABLED)
            
    def setTimeout(self, selection):
        lookup = {'Indefinite': None, '1 sec': 1,'5 sec': 5,'10 sec': 10,'20 sec': 20,'30 sec': 30, '1 min': 60}
        self.timeout = lookup[selection]








def eraseFiles():
    with open("moves.txt", 'w') as outfile:
        outfile.write("")
    with open("gamestate.txt", 'w') as outfile:
        outfile.write("")







if __name__ == "__main__":
    #---------Code for creating an instance of the window---------
    #erase the communication files to start fresh
    eraseFiles()

    #create a window
    window = tk.Tk()

    #set the title
    window.title("Welcome, master warrior, to Onitama")

    #set the default window size
    window.geometry('1200x600')

    #create an instance of the game
    game = Onitama(window)
    game.pack()

    #display the window
    window.mainloop()