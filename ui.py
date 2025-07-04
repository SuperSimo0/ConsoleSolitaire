from shutil import get_terminal_size
import colorama
from cards import cardDrawings

colorama.init() # Activate color codes support for most terminals


def renderWelcomeUi():
    """
    Prints the welcome UI
    :return:
    """

    welcome = '''\n\n\n
           ________________________________________________
          /                                                \\            /$$$$$$                                          /$$                  
         |    _________________________________________     |           /$$__  $$                                        | $$                  
         |   |                                         |    |          | $$  \\__/  /$$$$$$  /$$$$$$$   /$$$$$$$  /$$$$$$ | $$  /$$$$$$         
         |   |  C:\\> _                                 |    |          | $$       /$$__  $$| $$__  $$ /$$_____/ /$$__  $$| $$ /$$__  $$        
         |   |                                         |    |          | $$      | $$  \\ $$| $$  \\ $$|  $$$$$$ | $$  \\ $$| $$| $$$$$$$$        
         |   |                                         |    |          | $$    $$| $$  | $$| $$  | $$ \\____  $$| $$  | $$| $$| $$_____/        
         |   |                                         |    |          |  $$$$$$/|  $$$$$$/| $$  | $$ /$$$$$$$/|  $$$$$$/| $$|  $$$$$$$    
         |   |                                         |    |           \\______/  \\______/ |__/  |__/|_______/  \\______/ |__/ \\_______/        
         |   |                                         |    |
         |   |                                         |    |            /$$$$$$            /$$ /$$   /$$               /$$                    
         |   |                                         |    |           /$$__  $$          | $$|__/  | $$              |__/                    
         |   |                                         |    |          | $$  \\__/  /$$$$$$ | $$ /$$ /$$$$$$    /$$$$$$  /$$  /$$$$$$   /$$$$$$ 
         |   |                                         |    |          |  $$$$$$  /$$__  $$| $$| $$|_  $$_/   |____  $$| $$ /$$__  $$ /$$__  $$
         |   |_________________________________________|    |           \\____  $$| $$  \\ $$| $$| $$  | $$      /$$$$$$$| $$| $$  \\__/| $$$$$$$$
         |                                                  |           /$$  \\ $$| $$  | $$| $$| $$  | $$ /$$ /$$__  $$| $$| $$      | $$_____/
          \\_________________________________________________/          |  $$$$$$/|  $$$$$$/| $$| $$  |  $$$$/|  $$$$$$$| $$| $$      |  $$$$$$$
                 \\___________________________________/                  \\______/  \\______/ |__/|__/   \\___/   \\_______/|__/|__/       \\_______/
                                                                         Farina Simone\n\n\n\n\n\n\n
    
    
    
          Press any key to start a new game!
    '''

    # Print Welcome Message
    for line in welcome.split('\n'):
        print(('\033[48;5;235m' + line.ljust(get_terminal_size().columns)) + '\033[0m')
    for i in range(get_terminal_size().lines-len(welcome.split('\n'))):
        print(('\033[48;5;235m' + ''.ljust(get_terminal_size().columns)) + '\033[0m')

def representColumns(deck):
    """
    representColumns
    Having a 2D card array, it returns an array with the text representation of the array itself.
    :param deck: 2D list of cards
    :return: list of strings representing the columns. Each string represents a single column
    """
    columnRepresentation = ['' for _ in range(7)]  # columns

    for columnIndex in range(0, len(deck)):
        column = deck[columnIndex]
        if len(column) == 0:
            columnRepresentation[columnIndex] = " [EMPTY]  "
        for cardIndex in range(0, len(column)):
            card = column[cardIndex]
            lineList = []

            # Checking if the card should be seen
            if card.discovered:
                if cardIndex == len(column) - 1:
                    cardRepresentation = cardDrawings[card.value - 1].format(card.symbol).split('\n')
                else:
                    cardRepresentation = cardDrawings[-2].format(card.name[0], card.name[1]).split('\n')

                # little hack for the white card and the coloured text
                for line in cardRepresentation:
                    if card.isSelected:
                        cardColor = '48;5;159'
                    else:
                        cardColor = '48;5;231'

                    if card.symbol in ['♦', '♥']:
                        lineColor = '38;5;196'
                    else:
                        lineColor = '38;5;16'
                    lineList.append(f'\033[{lineColor};{cardColor}m{line}\033[0m')

                columnRepresentation[columnIndex] += '\n'.join(lineList)

            else:
                columnRepresentation[columnIndex] += cardDrawings[-1]

            columnRepresentation[columnIndex] += '\n'
            columnRepresentation[columnIndex] += '         \n'
        columnRepresentation[columnIndex] = columnRepresentation[columnIndex][:-1]
    return columnRepresentation


def getLines(deck):
    """
    getLines
    Having a 2D card array, it generates the list of lines to print as the deck UI
    :param deck:
    :return:
    """
    columnRepresentation = representColumns(deck)

    # Mixing and formatting the columns
    toPrint = ['']

    for columnIndex in range(0, len(deck)):
        column = columnRepresentation[columnIndex]
        currentLine = -1
        for line in column.split('\n'):
            currentLine += 1
            if len(toPrint) == currentLine:
                toPrint.append(' '*10*columnIndex)
            toPrint[currentLine] += line + ' '

        currentLine += 1
        while currentLine <= len(toPrint)-1:
            toPrint[currentLine] += ' '*10
            currentLine += 1

    return toPrint


def renderGameUi(gameObject, selectedColumn=None):
    """
    Given a game object and eventually a column to highlight, it renders (prints) the whole game UI.
    It will print both the deck UIs (the normal one and the winning columns), using colors.
    Unfortunately it was necessary to setup colorama, as mostly only IDEs support ANSI Escape Codes by default.
    :param gameObject: main solitaire game object
    :param selectedColumn: Used for highlighting columns
    :return:
    """

    deck = gameObject.columns
    winningDeck = gameObject.winningColumns
    normalDeckLines = getLines(deck)
    winningDeckLines = getLines(winningDeck)

    # Printing the message
    upperLine = ' '*10 + '┌' + '─'*72 + '┐' + ' '*10 + '┌' + '─'*42 + '┐' # Default if there is no selected line
    if selectedColumn is not None: # selectedColumn 0-6 (main), 7-10 (winning)
        if selectedColumn < 7: # Left
            upperLine = ' ' * 10 + '┌' + selectedColumn*10*'─' +'\033[48;5;159m' + ' '*9 + '\033[0m─' + (7-selectedColumn-1)*10*'─' + '──┐' + ' '*10 + '┌' + '─'*42 + '┐'
        if 7 <= selectedColumn <= 10: # Right
            selectedColumn = selectedColumn-7
            upperLine = ' ' * 10 + '┌' + '─' * 72 + '┐' + ' ' * 10 + '┌' + selectedColumn*10*'─' +'\033[48;5;159m' + ' '*9 + '\033[0m─' + (4-selectedColumn-1)*10*'─' + '──┐'
    print(upperLine)

    totalLines = max(len(normalDeckLines)+1, len(winningDeckLines)+1)
    for lineIndex in range(0, totalLines):
        # left side
        toPrint = ' '*84
        if lineIndex < len(normalDeckLines):
            normalDeckLine = normalDeckLines[lineIndex]
            toPrint = ' '*10 + '│' + normalDeckLine + ' '*2 + '│'
        if lineIndex == len(normalDeckLines):
            toPrint = ' ' * 10 + '└' + '─' * 72 + '┘'

        # right side
        if lineIndex < len(winningDeckLines):
            winningDeckLine = winningDeckLines[lineIndex]
            toPrint += ' ' * 10 + '│' + winningDeckLine + ' ' * 2 + '│'
        if lineIndex == len(winningDeckLines):
            toPrint += ' ' * 10 + '└' + '─' * 42 + '┘'
        print(toPrint)
    print()
    print(gameObject.instructionMessage)
    for i in range(get_terminal_size().lines-totalLines-len(gameObject.instructionMessage.split('\n'))-8):
        print()


defaultInstructions = '''To select one or more cards, use WASD.
A  ›  Move one column to the left
D  ›  Move one column to the right
W  ›  Select one more card on the same column
S  ›  Deselect the top card on the column
ENTER  ›  Confirm that you want to move the selected cards

P  ›  Draw a card from the deck
Z  ›  Surrender the game'''


def renderSurrenderMessage():
    """
        Prints the surrender message
        :return:
    """

    surrender = f'''\n\n\n
    
                   __
                  / \\--..____
                   \\ \\       \\-----,,,..
                    \\ \\       \\         \\--,,..
                     \\ \\       \\         \\  ,\'
                      \\ \\       \\         \\ ``..
                       \\ \\       \\         \\-\'\'
                        \\ \\       \\__,,--\'\'\'
                         \\ \\       \\.
                          \\ \\      ,/
                           \\ \\__..-
                            \\ \\
                             \\ \\
                              \\ \\   
                               \\ \\
                                \\ \\
                                 \\ \\
                                  \\ \\
                                   \\ \\
                                    \\ \\


  /$$$$$$  /$$   /$$ /$$$$$$$  /$$$$$$$  /$$$$$$$$ /$$   /$$ /$$$$$$$  /$$$$$$$$ /$$$$$$$  /$$$$$$$$ /$$$$$$$ 
 /$$__  $$| $$  | $$| $$__  $$| $$__  $$| $$_____/| $$$ | $$| $$__  $$| $$_____/| $$__  $$| $$_____/| $$__  $$
| $$  \\__/| $$  | $$| $$  \\ $$| $$  \\ $$| $$      | $$$$| $$| $$  \\ $$| $$      | $$  \\ $$| $$      | $$  \\ $$
|  $$$$$$ | $$  | $$| $$$$$$$/| $$$$$$$/| $$$$$   | $$ $$ $$| $$  | $$| $$$$$   | $$$$$$$/| $$$$$   | $$  | $$
 \\____  $$| $$  | $$| $$__  $$| $$__  $$| $$__/   | $$  $$$$| $$  | $$| $$__/   | $$__  $$| $$__/   | $$  | $$
 /$$  \\ $$| $$  | $$| $$  \\ $$| $$  \\ $$| $$      | $$\\  $$$| $$  | $$| $$      | $$  \\ $$| $$      | $$  | $$
|  $$$$$$/|  $$$$$$/| $$  | $$| $$  | $$| $$$$$$$$| $$ \\  $$| $$$$$$$/| $$$$$$$$| $$  | $$| $$$$$$$$| $$$$$$$/
 \\______/  \\______/ |__/  |__/|__/  |__/|________/|__/  \\__/|_______/ |________/|__/  |__/|________/|_______/ 

Wanna try again? 

'''

    # Print Colored Win Message
    for line in surrender.split('\n'):
        print(('\033[48;5;235m' + line.ljust(get_terminal_size().columns)) + '\033[0m')
    for i in range(get_terminal_size().lines - len(surrender.split('\n'))):
        print(('\033[48;5;235m' + ''.ljust(get_terminal_size().columns)) + '\033[0m')

def renderWinMessage(timeTaken):
    """
        Prints the win message
        :return:
    """

    win = f'''\n\n\n
                                     
                                     
                                  ___________                                        
                             .---'::'        `---.                                   |  $$   /$$//$$__  $$| $$  | $$      
                            (::::::'              )                                   \\  $$ /$$/| $$  \\ $$| $$  | $$      
                            |`-----._______.-----'|                                    \\  $$$$/ | $$  | $$| $$  | $$      
                            |              :::::::|                                     \\  $$/  | $$  | $$| $$  | $$      
                           .|               ::::::!-.                                    | $$   | $$  | $$| $$  | $$      
                           \\|               :::::/|/                                     | $$   |  $$$$$$/|  $$$$$$/      
                            |               ::::::|                                      |__/    \\______/  \\______/       
                            |      Final Time ::::|                                  
                            |     {str(timeTaken)} Seconds ::::|                                   /$$      /$$  /$$$$$$  /$$   /$$ /$$
                            |               ::::::|                                  | $$  /$ | $$ /$$__  $$| $$$ | $$| $$
                            |              .::::::|                                  | $$ /$$$| $$| $$  \\ $$| $$$$| $$| $$
                            J              :::::::F                                  | $$/$$ $$ $$| $$  | $$| $$ $$ $$| $$
                             \\            :::::::/                                   | $$$$_  $$$$| $$  | $$| $$  $$$$|__/
                              `.        .:::::::'                                    | $$$/ \\  $$$| $$  | $$| $$\\  $$$    
                                `-._  .::::::-'                                      | $$/   \\  $$|  $$$$$$/| $$ \\  $$ /$$
                                    |  """|"                                         |__/     \\__/ \\______/ |__/  \\__/|__/
                                    |  :::|                                          
                                    F   ::J                                          
                                   /     ::\\                                         
                              __.-'      :::`-.__                                    
                             (_           ::::::_)                                   
                               `"""---------"""'                                     
        '''

    # Print Colored Win Message
    for line in win.split('\n'):
        print(('\033[48;5;235m' + line.ljust(get_terminal_size().columns)) + '\033[0m')
    for i in range(get_terminal_size().lines - len(win.split('\n'))):
        print(('\033[48;5;235m' + ''.ljust(get_terminal_size().columns)) + '\033[0m')
