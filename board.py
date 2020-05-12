import tkinter as tk
import tkinter.messagebox
import cards
class Board(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        #colors
        self.color = "#efe5b0"
        self.shadeColor = "#b97957"
        self.selectColor = "#880015"

        #misc
        self.configure(bg=self.color)
        self.cards = cards.shuffle()
        self.turn = False #false is red's turn, true is blue

        #card slots
        self.redToBlue = CardSlot(self, [self.color, self.shadeColor, self.selectColor])
        self.redToBlue.disable()

        self.blue1 = CardSlot(self, [self.color, self.shadeColor, self.selectColor])
        self.blue1.disable()

        self.red1 = CardSlot(self, [self.color, self.shadeColor, self.selectColor])

        self.blue2 = CardSlot(self, [self.color, self.shadeColor, self.selectColor])
        self.blue2.disable()

        self.red2 = CardSlot(self, [self.color, self.shadeColor, self.selectColor])

        self.blueToRed = CardSlot(self, [self.color, self.shadeColor, self.selectColor])
        self.blueToRed.disable()

        #deal the cards into the slots. Note that the redToBlue slot STAYS EMPTY
        self.blue1.changeCard(self.cards[0])
        self.red1.changeCard(self.cards[1])
        self.blue2.changeCard(self.cards[2])
        self.red2.changeCard(self.cards[3])
        self.blueToRed.changeCard(self.cards[4])

        self.selectedCardSlot = 0 #null value

        #add click handlers to all the card slots
        self.redToBlue.butt.configure(command = lambda cardSlot=self.redToBlue: self.select(cardSlot))
        self.blue1.butt.configure(command = lambda cardSlot=self.blue1: self.select(cardSlot))
        self.red1.butt.configure(command = lambda cardSlot=self.red1: self.select(cardSlot))
        self.blue2.butt.configure(command = lambda cardSlot=self.blue2: self.select(cardSlot))
        self.red2.butt.configure(command = lambda cardSlot=self.red2: self.select(cardSlot))
        self.blueToRed.butt.configure(command = lambda cardSlot=self.blueToRed: self.select(cardSlot))

        self.redToBlue.grid(column=0, row=1)
        self.blue1.grid(column=1, row=0)
        self.red1.grid(column=1, row=2)

        self.innerBoard = InnerBoard(self, [self.color, self.shadeColor, self.selectColor], self.turn)
        self.innerBoard.grid(column=2, row=0, rowspan=3)

        self.blue2.grid(column=3, row=0)
        self.red2.grid(column=3, row=2)
        self.blueToRed.grid(column=4, row=1)

    def select(self, cardSlot):
        #can't select if the game is over
        if self.master.gameIsOver:
            return
        if(self.selectedCardSlot):
            self.selectedCardSlot.deselect() #set the previous selected cardSlot back to normal color
        if(self.selectedCardSlot is cardSlot):#if the user clicks the current selection, deselect it
            self.selectedCardSlot = 0
            self.innerBoard.selectedCard = 0
        else:
            print(f"cardSlot at {cardSlot.grid_info()['row']}, {cardSlot.grid_info()['column']} was selected")
            if cardSlot.card:
                self.selectedCardSlot = cardSlot
                self.innerBoard.selectedCard = cardSlot.card
                cardSlot.select()
            else:
                print("no card in slot")
        self.innerBoard.shadePossibleMoves()
    
    def changeTurn(self):
        if self.turn:
            if not self.master.redIsComputer:
                self.red1.enable()
                self.red2.enable()
            self.blue1.disable()
            self.blue2.disable()
        else:
            self.red1.disable()
            self.red2.disable()
            if not self.master.blueIsComputer:
                self.blue1.enable()
                self.blue2.enable()
        self.selectedCardSlot = 0
        self.turn = not self.turn
        self.innerBoard.changeTurn()
        if not self.master.gameIsOver:
            self.master.makeComputerMove()

    def makeMove(self, currLoc, moveTo, cardName):
        if self.isLegal(currLoc, moveTo, cardName):
            cardSlot = None
            if self.turn:
                if self.blue1.card.name == cardName:
                    cardSlot = self.blue1
                elif self.blue2.card.name == cardName:
                    cardSlot = self.blue2
                self.blueToRed.changeCard(cardSlot.card)
                cardSlot.changeCard(self.redToBlue.card)
                self.redToBlue.changeCard(0)
            else:
                if self.red1.card.name == cardName:
                    cardSlot = self.red1
                elif self.red2.card.name == cardName:
                    cardSlot = self.red2
                self.redToBlue.changeCard(cardSlot.card)
                cardSlot.changeCard(self.blueToRed.card)
                self.blueToRed.changeCard(0)
            self.innerBoard.movePiece(currLoc, moveTo)
            self.changeTurn()
            self.appendToMoves(currLoc, moveTo, cardName)


        else:
            print("ILLEGAL MOVE")
            tkinter.messagebox.showerror(title="Illegal Move", message=f"{'blue' if self.turn else 'red'} has made an ILLEGAL move. Game Over.")
            #self.master.control.goButton.configure(state=tk.NORMAL)
            self.master.gameIsOver = True
            self.master.gameIsRunning = False

    def isLegal(self, currLoc, moveTo, cardName):
        #first, make sure the positions are on the board
        buttonFrom = None
        buttonTo = None
        try:
            buttonFrom = self.innerBoard.matrix[int(currLoc[0])][int(currLoc[1])]
            buttonTo = self.innerBoard.matrix[int(moveTo[0])][int(moveTo[1])]
        except:
            print("index bad")
            print(currLoc)
            print(moveTo)
            return False

        #next, we make sure the card is a valid option, and get its move set
        card = None
        if self.turn:
            if self.blue1.card.name == cardName:
                card = self.blue1.card
            elif self.blue2.card.name == cardName:
                card = self.blue2.card
        else:
            if self.red1.card.name == cardName:
                card = self.red1.card
            elif self.red2.card.name == cardName:
                card = self.red2.card

        if(card is None):
            print(f"{cardName} is not a playable card")
            return False

        #next, lets check to make sure that the player has a peice at the starting position
        if self.turn:
            if not (buttonFrom.cget("image") == str(self.innerBoard.blueMaster) or buttonFrom.cget("image") == str(self.innerBoard.blueStudent)):
                print("no piece at start")
                return False
        else:
            if not (buttonFrom.cget("image") == str(self.innerBoard.redMaster) or buttonFrom.cget("image") == str(self.innerBoard.redStudent)):
                print("no piece at red start")
                return False

        #now we make sure the player can legally land on the end position:
        if self.turn:
            if buttonTo.cget("image") == str(self.innerBoard.blueMaster) or buttonTo.cget("image") == str(self.innerBoard.blueStudent):
                print("piece at end")
                return False
        else:
            if buttonTo.cget("image") == str(self.innerBoard.redMaster) or buttonTo.cget("image") == str(self.innerBoard.redStudent):
                print("piece at end")
                return False

        #now we check if that card can be used to make that move
        move = (moveTo[0] - currLoc[0], moveTo[1] - currLoc[1])
        if self.turn:
            move = (-move[0], -move[1]) #flip for blue
        if move in card.moves:
            return True
        else:
            print("move not found in card")
            return False

    def writeGameState(self):
        with open("gamestate.txt", "w") as outfile:
            for row in range(5):
                for col in range(5):
                    outchar = '-'
                    if(self.innerBoard.matrix[col][row].cget("image") == str(self.innerBoard.blueStudent)):
                       outchar = 'b' 
                    elif(self.innerBoard.matrix[col][row].cget("image") == str(self.innerBoard.blueMaster)):
                       outchar = 'B' 
                    elif(self.innerBoard.matrix[col][row].cget("image") == str(self.innerBoard.redStudent)):
                       outchar = 'r' 
                    elif(self.innerBoard.matrix[col][row].cget("image") == str(self.innerBoard.redMaster)):
                       outchar = 'R' 
                    outfile.write(outchar)
            outfile.write('\n' + self.blue1.card.name)
            outfile.write('\n' + self.blue2.card.name)
            outfile.write('\n' + self.red1.card.name)
            outfile.write('\n' + self.red2.card.name)
            if self.redToBlue.card:
                outfile.write('\n' + self.redToBlue.card.name + '\n')
            else:
                outfile.write('\n' + self.blueToRed.card.name + '\n')
            outfile.write(str(0) if self.turn else str(1))
        



    def appendToMoves(self, currLoc, moveTo, cardName):
        pass


        
        






class InnerBoard(tk.Frame):
    def __init__(self, parent, colors, turn):
        tk.Frame.__init__(self, parent)
        self.color = colors[0]
        self.shadeColor = colors[1]
        self.selectColor = colors[2]
        self.turn = turn

        self.selectedCard = 0 #the card currently selected, 0 if none

        self.blueMaster = tk.PhotoImage(file = "./img/master-blue-small.png")
        self.blueStudent = tk.PhotoImage(file = "./img/student-blue-small.png")
        self.redMaster = tk.PhotoImage(file = "./img/master-red-small.png")
        self.redStudent = tk.PhotoImage(file = "./img/student-red-small.png")
        self.blankimg = tk.PhotoImage(file = "./img/blank.png")

        self.matrix = [list(range(5)) for d in range(5)]
        self.selected = 0 #null value
        for col in range(5):
            for row in range(5):

                if row == 0:
                    if col == 2:
                        btn = tk.Button(self, image=self.blueMaster, bg="blue")
                    else:
                        btn = tk.Button(self, image=self.blueStudent, bg=self.color)
                elif row == 4:
                    if col == 2:
                        btn = tk.Button(self, image=self.redMaster, bg="red")
                    else:
                        btn = tk.Button(self, image=self.redStudent, bg=self.color)
                else:
                    btn = tk.Button(self, image=self.blankimg, bg=self.color)
                    
                btn.grid(column=col, row=row)
                btn.configure(command=lambda button=btn: self.select(button))
                self.matrix[col][row] = btn


    def select(self, button):
        #can't select if it is a computer's turn, or if the game is over
        if self.master.master.blueIsComputer and self.turn:
            return
        if self.master.master.redIsComputer and not self.turn:
            return
        if self.master.master.gameIsOver:
            return
        if (self.turn and (button.cget("image") == str(self.blueMaster) or button.cget("image") == str(self.blueStudent))) or (not self.turn and (button.cget("image") == str(self.redMaster) or button.cget("image") == str(self.redStudent))):
            if(self.selected):
                #set the previous selected button back to normal color
                if(self.selected.grid_info()['row'] == 4 and self.selected.grid_info()['column'] == 2):
                    self.selected.configure(bg = "red")#shrines are special colors
                elif(self.selected.grid_info()['row'] == 0 and self.selected.grid_info()['column'] == 2):
                    self.selected.configure(bg = "blue")
                else:
                    self.selected.configure(bg = self.color)
            if(self.selected is button):#if the user clicks the current selection, deselect it
                self.selected = 0
            else:
                self.selected = button
                button.configure(bg=self.selectColor)
            self.shadePossibleMoves()
        else:
            #check if the user is clicking a shaded space, and if so, make the move.
            if(button.cget("bg") == self.shadeColor):
                currLoc = (self.selected.grid_info()['column'], self.selected.grid_info()['row'])
                moveTo = (button.grid_info()['column'], button.grid_info()['row'])
                if not self.master.master.gameIsRunning:
                    print("autostart")
                    self.master.master.startGame()
                self.master.makeMove(currLoc, moveTo, self.selectedCard.name)


    def shadePossibleMoves(self):
        if self.selectedCard and self.selected and self.selected.cget("image") != str(self.blankimg):
            self.unshadeAll()
            row = self.selected.grid_info()['row']
            col = self.selected.grid_info()['column']
            flipper = -1 if self.turn else 1 #coeficient used to flip the move along the y axis if played by blue
            for ncol, nrow in self.selectedCard.moves:
                nrow = flipper*nrow
                ncol = flipper*ncol
                if col+ncol >= 0 and col+ncol < 5 and row+nrow >= 0 and row+nrow < 5:#if the row and col are valid
                    #if it is blue's turn, and the move won't land on a blue:
                    if  self.turn and self.matrix[col+ncol][row+nrow].cget("image") != str(self.blueMaster) and self.matrix[col+ncol][row+nrow].cget("image") != str(self.blueStudent):
                        self.matrix[col+ncol][row+nrow].configure(bg = self.shadeColor)
                    #elif it is red's turn, and the move won't land on a red:
                    elif  not self.turn and self.matrix[col+ncol][row+nrow].cget("image") != str(self.redMaster) and self.matrix[col+ncol][row+nrow].cget("image") != str(self.redStudent):
                        self.matrix[col+ncol][row+nrow].configure(bg = self.shadeColor)

        else:
            self.unshadeAll()

    def unshadeAll(self):
        for col in range(5):
            for row in range(5):
                if self.matrix[col][row].cget("bg") == self.shadeColor:
                    
                    if(row == 4 and col == 2):
                        self.matrix[col][row].configure(bg = "red")
                    elif(row == 0 and col == 2):
                        self.matrix[col][row].configure(bg = "blue")
                    else:
                        self.matrix[col][row].configure(bg = self.color)


    def getImage(self, imgString):
        if imgString == str(self.blueMaster):
            return self.blueMaster
        elif imgString == str(self.blueStudent):
            return self.blueStudent
        elif imgString == str(self.redMaster):
            return self.redMaster
        elif imgString == str(self.redStudent):
            return self.redStudent
        elif imgString == str(self.blankimg):
            return self.blankimg

    def movePiece(self, currLoc, moveTo):
        #note: this function does NO LEGALITY CHECKING. This function, if used wrong, easily breaks the game.
        past = self.matrix[currLoc[0]][currLoc[1]]
        future = self.matrix[moveTo[0]][moveTo[1]]
        future.configure(image=self.getImage(past.cget("image")))
        past.configure(image=self.blankimg)

    def changeTurn(self):
        self.turn = not self.turn
        #set the previous selected button back to normal color
        if self.selected:
            if(self.selected.grid_info()['row'] == 4 and self.selected.grid_info()['column'] == 2):
                self.selected.configure(bg = "red")#shrines are special colors
            elif(self.selected.grid_info()['row'] == 0 and self.selected.grid_info()['column'] == 2):
                self.selected.configure(bg = "blue")
            else:
                self.selected.configure(bg = self.color)

        self.unshadeAll()
        self.selected = 0
        self.selectedCard = 0
        self.checkForWinner()

    def checkForWinner(self):
        winner = None #assume there is not yet a winner
        blueMast = False
        redMast = False
        for col in range(5):
            for row in range(5):
                btn = self.matrix[col][row]
                #scan for masters (way of stone)
                if btn.cget("image") == str(self.redMaster):
                    redMast = True
                elif btn.cget("image") == str(self.blueMaster):
                    blueMast = True

                #check for way of stream
                if row == 0 and col == 2:
                    if btn.cget("image") == str(self.redMaster):
                        winner = "red has won by way of the stream"
                elif row == 4 and col == 2:
                    if btn.cget("image") == str(self.blueMaster):
                        winner = "blue has won by way of the stream"
                else:
                    btn = tk.Button(self, image=self.blankimg, bg=self.color)
                
        #check for way of the stone
        if not redMast:
            winner = "blue has won by way of the stone"
        elif not blueMast:
            winner = "red has won by way of the stone"
        
        if(winner):
            tkinter.messagebox.showinfo(title="Winner", message=winner)
            self.master.master.gameIsOver = True

        return winner

                
        










class CardSlot(tk.Frame):  #holds and displays cards, but also exists as its own object.
    def __init__(self, parent, colors):
        tk.Frame.__init__(self, parent)
        self.color = colors[0]
        self.shadeColor = colors[1]
        self.selectColor = colors[2]
        self.card = 0
        self.blankimg = tk.PhotoImage(file = "./img/card-blank.png")
        self.butt = tk.Button(self, bg=self.color)
        self.butt.grid(row=0, column=0, ipady=10, ipadx=10)
        self.changeCard(0)
        

    def changeCard(self, card):
        self.card = card
        if(self.card):
            self.butt.config(image=self.card.img, relief='raised')
        else:
            self.butt.config(image=self.blankimg, relief='flat')
    
    def select(self):
        self.butt.config(bg=self.selectColor)

    def deselect(self):
        self.butt.config(bg=self.color)

    def disable(self):
        self.deselect()
        self.butt.configure(state=tk.DISABLED)
    
    def enable(self):
        self.butt.configure(state=tk.NORMAL)