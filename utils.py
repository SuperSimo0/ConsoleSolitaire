def clearScreen():
    """
    Clear screen using ANSI codes
    :return:
    """
    print('\033[2J') # https://stackoverflow.com/questions/37774983/clearing-the-screen-by-printing-a-character

def redColor(line):
    """
    Turn the given line red.
    :param line:
    :return:
    """
    return f'\033[38;5;160m{line}\033[0m'