import time
from ui import renderWelcomeUi, renderGameUi, defaultInstructions, renderSurrenderMessage, renderWinMessage
from utils import clearScreen, redColor
from gameclasses import Game
from gamefunctions import handleSelectionLeft, handleSelectionRight, handleSelectionUp, handleSelectionDown, handleMovingSelection, handleDraw
from readchar import readkey, key

def main():
    clearScreen()
    renderWelcomeUi()
    readkey() # One-letter input without pressing enter https://pypi.org/project/readchar/

    solitaireGame = Game() # Creating a new game object
    startTime = time.time()
    # instructions on the lower side of the game
    solitaireGame.instructionMessage = defaultInstructions

    # default selection (for the purpose of simplicity, there will always be at least one card selected)
    solitaireGame.select(0, 0) # 1st column, 1st card

    playing = True
    surrender = False
    while playing:
        if solitaireGame.gameWon(): # checking if player already won
            playing = False
        clearScreen()
        renderGameUi(solitaireGame)
        if playing:
            cmd = readkey().lower()
        else:
            cmd = ""

        match cmd:
            case 'a': # move to the left
                handleSelectionLeft(solitaireGame)
            case 'd':  # move to the right
                handleSelectionRight(solitaireGame)
            case 'w': # move up
                handleSelectionUp(solitaireGame)
            case 's': # move down
                handleSelectionDown(solitaireGame)
            case '\r' | '\n': # move cards (i hate different OSes. Windows needs \r, linux needs \n)
                handleMovingSelection(solitaireGame)
            case 'p': #draw
                handleDraw(solitaireGame)
            case 'z':
                print('Are you sure that you want to surrender? Press "y" to confirm')
                confirmation = readkey().lower()
                if confirmation == 'y':
                    playing = False
                    surrender = True

    endTime = time.time()
    elapsedTime = endTime - startTime
    if surrender:
        renderSurrenderMessage()
    else:
        clearScreen()
        renderWinMessage(int(elapsedTime))

if __name__ == '__main__':
    main()