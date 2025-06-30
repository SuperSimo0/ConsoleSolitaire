def clearScreen():
    print('\x1b[2J')

def redColor(line):
    return f'\033[38;5;160m{line}\033[0m'