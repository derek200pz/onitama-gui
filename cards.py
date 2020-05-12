import tkinter as tk
import random

class Card():
    def __init__(self, moves, imgPath, name):
        self.name = name
        self.moves = moves
        self.img = tk.PhotoImage(file = imgPath)
        

def shuffle():

    cards = [
        Card([(0, 1), (0, -2)], "./img/card-tiger-small.png", "Tiger"),
        Card([(-2, -1), (-1, 1), (1, 1), (2, -1)], "./img/card-dragon-small.png", "Dragon"),
        Card([(-2, 0), (-1, -1), (1, 1)], "./img/card-frog-small.png", "Frog"),
        Card([(-1, 1), (1, -1), (2, 0)], "./img/card-rabbit-small.png", "Rabbit"),
        Card([(-2, 0), (0, -1), (2, 0)], "./img/card-crab-small.png", "Crab"),
        Card([(-1, -1), (-1, 0), (1, 0), (1, -1)], "./img/card-elephant-small.png", "Elephant"),
        Card([(-1, -1), (-1, 0), (1, 0), (1, 1)], "./img/card-goose-small.png", "Goose"),
        Card([(-1, 0), (-1, 1), (1, 0), (1, -1)], "./img/card-rooster-small.png", "Rooster"),
        Card([(-1, -1), (-1, 1), (1, -1), (1, 1)], "./img/card-monkey-small.png", "Monkey" ),
        Card([(-1, -1), (1, -1), (0, 1)], "./img/card-mantis-small.png", "Mantis" ),
        Card([(-1, 0), (0, -1), (0, 1)], "./img/card-horse-small.png", "Horse" ),
        Card([(0, -1), (0, 1), (1, 0)], "./img/card-ox-small.png", "Ox" ),
        Card([(0, -1), (-1, 1), (1, 1)], "./img/card-crane-small.png", "Crane" ),
        Card([(-1, 0), (0, -1), (1, 0)], "./img/card-boar-small.png", "Boar" ),
        Card([(-1, -1), (-1, 1), (1, 0)], "./img/card-eel-small.png", "Eel" ),
        Card([(-1, 0), (1, -1), (1, 1)], "./img/card-cobra-small.png", "Cobra" )
    ]

    #return a list of 5 cards
    return(random.sample(cards, 5))