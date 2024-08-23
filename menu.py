import re
from os import name, system

class Menu:
    """
    A class that creates interactive beautiful menus.
    """
    __ranges = [
        {"from": "\u3300", "to": "\u33ff"},         # compatibility ideographs
        {"from": "\ufe30", "to": "\ufe4f"},         # compatibility ideographs
        {"from": "\uf900", "to": "\ufaff"},         # compatibility ideographs
        {"from": "\U0002F800", "to": "\U0002fa1f"}, # compatibility ideographs
        {'from': "\u3040", 'to': "\u309f"},         # Japanese Hiragana
        {"from": "\u30a0", "to": "\u30ff"},         # Japanese Katakana
        {"from": "\u2e80", "to": "\u2eff"},         # cjk radicals supplement
        {"from": "\u4e00", "to": "\u9fff"},
        {"from": "\u3400", "to": "\u4dbf"},
        {"from": "\U00020000", "to": "\U0002a6df"},
        {"from": "\U0002a700", "to": "\U0002b73f"},
        {"from": "\U0002b740", "to": "\U0002b81f"},
        {"from": "\U0002b820", "to": "\U0002ceaf"}  # included as of Unicode 8.0
    ]

    def __init__(self, maxLength, title="", sep=" "):
        """
        Initializes a Menu object.

        Parameters:
            maxLength (int): the number of maximum characters in one line
            title (str): title of the menu
            sep (str): a character used to seperate the title from its content
        """
        self.__maxLength = maxLength
        self.__title = title
        self.__sep = "|" + sep*(maxLength-2) + "|"
        self.__lines = []
        self.__counter = 0
        self.__border = "+" + "-"*(maxLength-2) + "+"
        self.__checkFormat(title)
        self.__content = []

    def addLines(self, text=""):
        """
        Add one or more lines to the menu.

        Parameters:
            text (str): line(s) to add
        """
        map(self.__checkFormat,text.split("\n"))
        self.__lines.extend([line for line in text.split("\n")])

    def addList(self, text):
        """
        Add a numbered list formatted line to the menu.

        Parameters:
            text (str): content of the list
        """
        self.__counter += 1
        
        line = f"{self.__counter}. {text}"
        self.__checkFormat(line)
        self.__lines.append(line)

    def setTitle(self, title):
        """
        Changes the title of the menu.

        Parameters:
            title (str): new title of the menu.
        """
        self.__title = title

    def show(self):
        """
        Print the menu to the screen.
        """
        Menu.clear()
        self.__format()
        print(self.__border)
        for c in self.__content:
            print(c)
        print(self.__border)

    @staticmethod
    def getChoice(choices):
        """
        Returns an integer of user's input if it is in a given range, else -1.

        Parameters:
            choices (int): max value in range. The range will be [1, choices]
        """
        key = input(f"Enter a number (1-{choices}): ")
        return int(key) if key in [*map(str, range(1,choices+1))] else -1

    @staticmethod
    def getKeyLog(text, empty=True):
        """
        Returns user's input.

        Parameters:
            text (str): the message indicating that the program is waiting for user's input
            empty (bool): whether the program accepts empty input or not. Default=True
        """
        inp = input(f"{text}: ")
        if not empty and inp=="":
            raise ValueError("Cannot enter empty string.")
        return inp
    @staticmethod
    def clear():
        """
        A function that clears the console screen.
        """
        if name == "nt":
            _ = system("cls")
        else:
            _ = system("clear")

    @staticmethod
    def logError(error):
        """
        Logs error to screen.

        Parameters:
            error (str): Error message to be logged
        """
        Menu.clear()
        print(f"Error: {error}")
        input()

    @staticmethod
    def __calcLen(line):
        """
        Calculate the length of the line. This function covers the situations in which the line contains special characters.
        """
        pattern = []
        for r in Menu.__ranges:
            pattern.append("["+r["from"]+"-"+r["to"]+"]")
        pattern = re.compile("|".join(pattern))
        res = re.findall(pattern, line)
        return len(line) - line.count("\x1b[6;30;42m")*14 + len(res)

    def __format(self):
        """
        Formats the whole menu content.
        """
        self.__content = []
        anchor = (self.__maxLength-2)//2 - len(self.__title)//2
        self.__content.append("|" + " "*anchor + self.__title + " "*(self.__maxLength-2-anchor-len(self.__title)) + "|")
        if len(self.__lines) != 0:
            self.__content.append(self.__sep)
        for i in range(len(self.__lines)):
            self.__content.append("|" + " " + self.__lines[i] + " "*(self.__maxLength-3-Menu.__calcLen(self.__lines[i])) + "|")

    def __checkFormat(self, line):
        """
        Checks if the length of the line surpasses provided max length. If fails, raise error.

        Parameters:
            line (str): the line to be checked
        """
        if Menu.__calcLen(line) > self.__maxLength-2:
            raise ValueError("Line too long")
