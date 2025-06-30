from ui import defaultInstructions, renderGameUi
from utils import redColor, clearScreen
from readchar import readkey, key

def handleSelectionLeft(solitaireGame):
    """
    Move the selection one row to the left.
    :param solitaireGame: main solitaire object
    :return:
    """

    x = solitaireGame.lastSelection[0]
    if x == 0:
        solitaireGame.instructionMessage = defaultInstructions + '\n\n' + redColor(
            'You are already at the leftmost card!')
        return

    solitaireGame.instructionMessage = defaultInstructions

    if x < 7:
        if len(solitaireGame.columns[x - 1]) != 0:  # if the column we're trying to go to is not empty
            solitaireGame.deselectColumn(x)  # deselecting the previously selected column
            solitaireGame.select(x - 1, len(solitaireGame.columns[x - 1]) - 1)
            return
    if x == 7:
        if len(solitaireGame.columns[x - 1]) != 0:  # if the column we're trying to go to is not empty
            solitaireGame.deselectWinningColumn(x)  # deselecting the previously selected column
            solitaireGame.select(x - 1, len(solitaireGame.columns[x - 1]) - 1)
            return
    if x > 7:
        if len(solitaireGame.winningColumns[x - 8]) != 0:  # if the column we're trying to go to is not empty
            solitaireGame.deselectWinningColumn(x)  # deselecting the previously selected column
            solitaireGame.selectWinning(x - 1)
            return

    # if it's empty
    columnNum = x - 1
    while columnNum > 7:
        columnNum -= 1
        if len(solitaireGame.winningColumns[
                   columnNum - 7]) != 0:  # if we can actually find a left column that's not empty
            if x > 6:
                solitaireGame.deselectWinningColumn(x)  # deselecting the previously selected column
            else:
                solitaireGame.deselectColumn(x)  # deselecting the previously selected column
            solitaireGame.selectWinning(columnNum)
            return

    while columnNum > 0:
        columnNum -= 1
        if len(solitaireGame.columns[columnNum]) != 0:  # if we can actually find a left column that's not empty
            if x > 6:
                solitaireGame.deselectWinningColumn(x)
            else:
                solitaireGame.deselectColumn(x)  # deselecting the previously selected column
            solitaireGame.select(columnNum, len(solitaireGame.columns[columnNum]) - 1)
            return
    solitaireGame.instructionMessage = defaultInstructions + '\n\n' + redColor(
        'You are at the rightmost card: The other columns are empty!')

def handleSelectionRight(solitaireGame):
    """
        Move the selection one row to the right.
        :param solitaireGame: main solitaire object
        :return:
    """
    x = solitaireGame.lastSelection[0]
    if x == 10:
        solitaireGame.instructionMessage = defaultInstructions + '\n\n' + redColor(
            'You are already at the rightmost card!')
        return

    solitaireGame.instructionMessage = defaultInstructions

    if x < 6:
        if len(solitaireGame.columns[x + 1]) != 0:  # if the column we're trying to go to is not empty
            solitaireGame.deselectColumn(x)  # deselecting the previously selected column
            solitaireGame.select(x + 1, len(solitaireGame.columns[x + 1]) - 1)
            return
    if x == 6:
        if len(solitaireGame.winningColumns[x - 6]) != 0:  # if the column we're trying to go to is not empty
            solitaireGame.deselectColumn(x)  # deselecting the previously selected column
            solitaireGame.selectWinning(x + 1)
            return
    if x > 6:
        if len(solitaireGame.winningColumns[x - 6]) != 0:  # if the column we're trying to go to is not empty
            solitaireGame.deselectWinningColumn(x)  # deselecting the previously selected column
            solitaireGame.selectWinning(x + 1)
            return

    # if it's empty
    columnNum = x + 1
    while columnNum < 6:
        columnNum += 1
        if len(solitaireGame.columns[columnNum]) != 0:  # if we can actually find a left column that's not empty
            solitaireGame.deselectColumn(x)  # deselecting the previously selected column
            solitaireGame.select(columnNum, len(solitaireGame.columns[columnNum]) - 1)
            return
    while columnNum < 10:
        columnNum += 1
        if len(solitaireGame.winningColumns[
                   columnNum - 7]) != 0:  # if we can actually find a left column that's not empty
            if x > 6:
                solitaireGame.deselectWinningColumn(x)  # deselecting the previously selected column
            else:
                solitaireGame.deselectColumn(x)  # deselecting the previously selected column
            solitaireGame.selectWinning(columnNum)
            return
    solitaireGame.instructionMessage = defaultInstructions + '\n\n' + redColor(
        'You are already at the rightmost card!\nThe other columns are empty!')

def handleSelectionUp(solitaireGame):
    """
        Move the selection one row up
        :param solitaireGame: main solitaire object
        :return:
    """
    x, y = solitaireGame.lastSelection

    if x > 6:
        solitaireGame.instructionMessage = defaultInstructions + '\n\n' + redColor(
            'You can\'t select more than one card in special columns!')
        return

    if y == 0:
        solitaireGame.instructionMessage = defaultInstructions + '\n\n' + redColor('You are already at the top card!')
        return

    upperCard = solitaireGame.columns[x][y - 1]
    if not upperCard.hasBeenDiscovered():
        solitaireGame.instructionMessage = defaultInstructions + '\n\n' + redColor(
            'You can\'t select a card you didn\'t discover')
        return

    solitaireGame.select(x, y - 1)
    solitaireGame.instructionMessage = defaultInstructions

def handleSelectionDown(solitaireGame):
    """
        Move the selection one row down
        :param solitaireGame: main solitaire object
        :return:
    """
    x, y = solitaireGame.lastSelection

    if x > 6:
        solitaireGame.instructionMessage = defaultInstructions + '\n\n' + redColor(
            'You can\'t select more than one card in special columns!')
        return

    if y == len(solitaireGame.columns[x]) - 1:
        solitaireGame.instructionMessage = defaultInstructions + '\n\n' + redColor(
            'You are already at the bottom card!')
        return
    solitaireGame.deselect(x, y)
    solitaireGame.instructionMessage = defaultInstructions

def handleMovingSelection(solitaireGame):
    """
    Full handler to move the column seletion.
    Used to pick the column where to place cards
    :param solitaireGame: main solitaire object
    :return:
    """

    solitaireGame.instructionMessage = defaultInstructions + '\n\n' + redColor(
        'Now please select the column where you want to put the selected card(s).\nPress q to cancel')
    clearScreen()
    selectedColumn = 0
    renderGameUi(solitaireGame, selectedColumn)
    columnCmd = ''
    while columnCmd not in ['\r', '\n']:
        columnCmd = readkey().lower()
        if columnCmd == 'a':
            if selectedColumn != 0:
                selectedColumn -= 1
            else:
                solitaireGame.instructionMessage = defaultInstructions + '\n\n' + redColor(
                    'You are already at the leftmost column!')
        if columnCmd == 'd':
            if selectedColumn != 10:
                selectedColumn += 1
            else:
                solitaireGame.instructionMessage = defaultInstructions + '\n\n' + redColor(
                    'You are already at the rightmost column!')
        if columnCmd == 'q':
            solitaireGame.instructionMessage = defaultInstructions
            return
        clearScreen()
        renderGameUi(solitaireGame, selectedColumn)
        solitaireGame.instructionMessage = defaultInstructions + '\n\n' + redColor(
            'Now please select the column where you want to put the selected card(s).\nPress q to cancel')
    solitaireGame.tryMoving(selectedColumn)
    return

def handleDraw(solitaireGame):
    """
    Main handler for drawing cards from the deck.
    It handles both the drawing and the positioning
    :param solitaireGame: main solitaire object
    :return:
    """
    if len(solitaireGame.remainingDeck) == 0:
        if len(solitaireGame.discarded) == 0:  # no more cards, both in the deck and in the discarded list
            solitaireGame.instructionMessage = defaultInstructions + '\n\n' + redColor(
                'There are no more cards in the deck.')
            return
        # no more cards in the deck but the discarded list is full. we need to shuffle it.
        solitaireGame.shuffleDiscarded()

    pickedCard = solitaireGame.remainingDeck[-1]  # picking card
    solitaireGame.remainingDeck = solitaireGame.remainingDeck[:-1]  # remove it from the deck
    solitaireGame.instructionMessage = defaultInstructions + '\n\n' + redColor(
        f'You got a {pickedCard.name} from the deck. Now select the column where you want to put the card.\nIf you want, Press q to discard it')

    done = False
    while not done:
        clearScreen()
        renderGameUi(solitaireGame)
        columnCmd = ''
        selectedColumn = 0

        # column selector
        while columnCmd not in ['\r', '\n']: # different os support
            columnCmd = readkey().lower()
            if columnCmd == 'a': # left
                if selectedColumn != 0:
                    selectedColumn -= 1
                else:
                    solitaireGame.instructionMessage = defaultInstructions + '\n\n' + redColor(
                        'You are already at the leftmost column!')
            if columnCmd == 'd': # right
                if selectedColumn != 10:
                    selectedColumn += 1
                else:
                    solitaireGame.instructionMessage = defaultInstructions + '\n\n' + redColor(
                        'You are already at the rightmost column!')
            if columnCmd == 'q': # discard
                solitaireGame.instructionMessage = defaultInstructions
                solitaireGame.discarded.append(pickedCard)
                done = True
                break
            clearScreen()
            renderGameUi(solitaireGame, selectedColumn)
            solitaireGame.instructionMessage = defaultInstructions + '\n\n' + redColor(
                f'You got a {pickedCard.name} from the deck. Now select the column where you want to put the card.\nIf you want, Press q to discard it')

        if done:
            break


        pickedCard.setVisible() # fix picked card not visible bug

        if selectedColumn < 7: # normal columns

            if len(solitaireGame.columns[selectedColumn]) == 0:  # first card in normal column
                if pickedCard.value != 13:
                    solitaireGame.instructionMessage = defaultInstructions + '\n\n' + redColor(
                        f'You can\'t move a card that isn\'t a king (value: 13) here')
                else:
                    solitaireGame.columns[selectedColumn].append(pickedCard)
                    solitaireGame.instructionMessage = defaultInstructions
                    done = True

            else:  # more than a card in normal column
                if pickedCard.value != solitaireGame.columns[selectedColumn][-1].value - 1: # check for value
                    solitaireGame.instructionMessage = defaultInstructions + '\n\n' + redColor(
                        f'You can\'t move a card that isn\'t of value {str(solitaireGame.columns[selectedColumn][-1].value - 1)} here')
                else:
                    if (not (pickedCard.symbol in ['♦', '♥']) and solitaireGame.columns[selectedColumn][-1].symbol in [
                        '♦', '♥']) or (pickedCard.symbol in ['♦', '♥'] and not (
                            solitaireGame.columns[selectedColumn][-1].symbol in ['♦', '♥'])): #check for symbol
                        solitaireGame.columns[selectedColumn].append(pickedCard)
                        solitaireGame.instructionMessage = defaultInstructions
                        done = True
                    else:
                        solitaireGame.instructionMessage = defaultInstructions + '\n\n' + redColor(
                            f'You can\'t move a card that is the same color of the last one in the column')

        else: # winning columns
            if len(solitaireGame.winningColumns[selectedColumn - 7]) == 0:  # first card in special column
                if pickedCard.value != 1:
                    solitaireGame.instructionMessage = defaultInstructions + '\n\n' + redColor(
                        f'You can\'t move a card that isn\'t an ace (value: 1) here')
                else:
                    solitaireGame.winningColumns[selectedColumn - 7].append(pickedCard)
                    solitaireGame.instructionMessage = defaultInstructions
                    done = True

            else:  # more than a card in a special column
                if pickedCard.value != solitaireGame.winningColumns[selectedColumn - 7][-1].value + 1:
                    solitaireGame.instructionMessage = defaultInstructions + '\n\n' + redColor(
                        f'You can\'t move a card that isn\'t of value {str(solitaireGame.winningColumns[selectedColumn - 7][-1].value + 1)} here')
                else:
                    if pickedCard.symbol == solitaireGame.winningColumns[selectedColumn - 7][-1].symbol:
                        solitaireGame.winningColumns[selectedColumn - 7].append(pickedCard)
                        solitaireGame.instructionMessage = defaultInstructions
                        done = True
                    else:
                        solitaireGame.instructionMessage = defaultInstructions + '\n\n' + redColor(
                            f'You can\'t have different symbols in a special column')
