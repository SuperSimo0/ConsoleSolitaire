import random
from utils import redColor
from ui import defaultInstructions

class Card:
    def __init__(self, symbol, name, value, discovered):
        self.symbol = symbol
        self.name = name
        self.value = value
        self.discovered = discovered
        self.isSelected = False

    def hasBeenDiscovered(self):
        return self.discovered

    def setVisible(self):
        self.discovered = True


class Game:
    def __init__(self):
        # Constants
        symbols = ['♥', '♦', '♠', '♣']
        values = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'X', 'Q', 'K']

        # Card Generation
        cards = []
        for symbol in symbols:
            for value in range(1, len(values) + 1):
                cards.append(Card(
                    symbol=symbol,
                    name=values[value - 1] + symbol,
                    value=value,
                    discovered=False
                ))

        # Deck Shuffling
        random.shuffle(cards)
        columns = []
        start = 0

        for index in range(1, 8):
            end = start + index
            columns.append(cards[start:end])
            start = end

        for column in columns:
            column[-1].setVisible()

        # Fixing the Object
        self.columns = columns
        self.remainingDeck = cards[28:]
        self.discarded = []
        self.winningColumns = [[], [], [], []]
        self.cardsInHand = []
        self.instructionMessage = ""
        self.lastSelection = ()

    def select(self, x, y):
        if x < len(self.columns):
            if y < len(self.columns[x]):
                self.columns[x][y].isSelected = True
                self.lastSelection = (x, y)

    def deselect(self, x, y):
        if x < len(self.columns):
            if y+1 < len(self.columns[x]):
                self.columns[x][y].isSelected = False
                self.columns[x][y+1].isSelected = True

        self.lastSelection = (x, y+1)

    def selectWinning(self, x):
        self.lastSelection = (x, -1)
        x -= 7
        self.winningColumns[x][-1].isSelected = True

    def deselectColumn(self, x):
        for cardIndex in range(0, len(self.columns[x])):
            card = self.columns[x][cardIndex]
            card.isSelected = False

    def deselectWinningColumn(self, x):
        x -= 7
        for card in self.winningColumns[x]:
            card.isSelected = False

    def shuffleDiscarded(self):
        self.remainingDeck = self.discarded
        self.discarded = []
        random.shuffle(self.remainingDeck)

    def tryMoving(self, columnNumber):
        # returns True if successful, False if not

        x, y = self.lastSelection
        print(x)
        print(y)
        if x < 7:
            firstCardToMove = self.columns[x][y]
        else:
            firstCardToMove = self.winningColumns[x-7][y]

        if columnNumber < 7: # Logic for the normal columns
            if len(self.columns[columnNumber]) == 0: #Logic for empty columns
                if firstCardToMove.value != 12:
                    self.instructionMessage = defaultInstructions + '\n\n' + redColor(
                        'You can\'t move a series of card(s) that doesn\'t start with a king into an empty column')
                    return False

                if x<7:
                    self.deselectColumn(x)
                    self.columns[columnNumber] += self.columns[x][y:]
                    self.columns[x] = self.columns[x][:y]
                    if len(self.columns[x]) != 0:
                        self.columns[x][-1].setVisible()
                else:
                    self.deselectWinningColumn(x)
                    self.columns[columnNumber] += self.winningColumns[x-7][y:]
                    self.winningColumns[x-7] = self.winningColumns[x-7][:y]
                    if len(self.winningColumns[x-7]) != 0:
                        self.winningColumns[x-7][-1].setVisible()

                self.select(columnNumber, len(self.columns[columnNumber]))
                return True

            lastCard = self.columns[columnNumber][-1]


            # Verify the value (lastCard > firstCardToMove)
            if lastCard.value-1 != firstCardToMove.value:
                self.instructionMessage = defaultInstructions + '\n\n' + redColor(
                    f'You can\'t move a card that isn\'t of value {str(lastCard.value-1)} here')
                return False

            redSymbols = ['♦', '♥']
            # Verify the type (alternate colors)
            if lastCard.symbol in redSymbols and firstCardToMove.symbol in redSymbols:  # if they're both red
                self.instructionMessage = defaultInstructions + '\n\n' + redColor(
                    'You can\'t move a card that is the same color as the chosen column\'s last card\'s value')
                return False
            if not(lastCard.symbol in redSymbols) and not(firstCardToMove.symbol in redSymbols): # if they're both black
                self.instructionMessage = defaultInstructions + '\n\n' + redColor(
                    'You can\'t move a card that is the same color as the chosen column\'s last card\'s value')
                return False


            if x<7:
                self.deselectColumn(x)
                self.columns[columnNumber] += self.columns[x][y:]
                self.columns[x] = self.columns[x][:y]
                if len(self.columns[x]) != 0:
                    self.columns[x][-1].setVisible()
            else:
                self.deselectWinningColumn(x)
                x = x-7
                self.columns[columnNumber] += self.winningColumns[x][y:]
                self.winningColumns[x] = self.winningColumns[x][:y]
                if len(self.winningColumns[x]) != 0:
                    self.winningColumns[x][-1].setVisible()
            self.select(columnNumber, len(self.columns[columnNumber]))
            return True


        if columnNumber >= 7: # Logic for the winning columns
            columnNumber -= 7
            if y != len(self.columns[x])-1:
                self.instructionMessage = defaultInstructions + '\n\n' + redColor(
                    'You can\'t move more than one card at a time into the winning columns')
                return False

            if len(self.winningColumns[columnNumber]) == 0: # Empty winning column logic - needs to start with ace, so what we can do 1 - 2 - 3 - etc
                if firstCardToMove.value != 1:
                    self.instructionMessage = defaultInstructions + '\n\n' + redColor(
                        'You need to start a winning column with an ace!')
                    return False

                # moving
                self.winningColumns[columnNumber].append(self.columns[x][-1])
                self.columns[x] = self.columns[x][:-1]
                self.winningColumns[columnNumber][-1].isSelected = False
                if len(self.columns[x]) != 0:
                    self.columns[x][-1].setVisible()
                print(columnNumber)
                print('aa')
                self.selectWinning(columnNumber+7)
                return True

            # logic if there's something already in the column
            if firstCardToMove.symbol != self.winningColumns[columnNumber][-1].symbol: # symbol check
                self.instructionMessage = defaultInstructions + '\n\n' + redColor(
                    'You can only have one symbol for each winning column!')
                return False

            if firstCardToMove.value != self.winningColumns[columnNumber][-1].value + 1: # value check
                self.instructionMessage = defaultInstructions + '\n\n' + redColor(
                    f'You can\'t insert this card here. You can only insert a card with a value of {str(self.winningColumns[columnNumber][-1].value + 1)}')
                return False

            # actual move
            self.winningColumns[columnNumber].append(self.columns[x][-1])
            self.columns[x] = self.columns[x][:-1]
            self.winningColumns[columnNumber][-1].isSelected = False
            if len(self.columns[x]) != 0:
                self.columns[x][-1].setVisible()
            self.selectWinning(columnNumber+7)
            return True

    