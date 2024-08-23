from abc import ABC, abstractmethod
import json
import re

class Catalog:
    """
    A class that simulates a library catalog and its functionality to track available items in the library.
    """

    def __init__(self, dataPath):
        """
        Initializes a Catalog object.

        Parameters:
            dataPath: The path to a json file containing information about library items
        """
        self.__dataPath = dataPath
        with open(dataPath) as file:
            self.__data = json.load(file)

        self.__items = []
        self.__update()

    @staticmethod
    def convert(data):
        """
        Returns a formatted string containing information of all items in list of data dictionary.

        Parameters:
            data (list): List of items whose information is in dictionaries

        Returns:
            res (str): Formatted string of data
        """
        res = []
        for d in data:
            r = ""
            for i in d:
                r += f"{i}: {d[i]}\n"
            res.append(r)
        res = "\n".join(res)
        return res
    
    def search(self, keyword, field=None):
        """
        Finds all items that matches with the provided keyword.

        Parameters:
            keyword (str): The keyword to search for
            field (str): The field in which the function searches. If None, the function will search all fields

        Returns:
            results (list): List of all library items that matches the keyword
        """
        if keyword == "":
            raise ValueError("Invalid Value.")

        results = []

        for item in self.__items:
            information = item.locate()
            foundDF = False
            if field == "Contributor":
                for t in item.getContribTypes():
                    if re.search(keyword, information[t], flags=re.IGNORECASE) is not None:
                        information[t] = re.sub(keyword, self.__f, information[t], flags=re.IGNORECASE)
                        foundDF = True
            elif field is not None:
                if re.search(keyword, information[field], flags=re.IGNORECASE) is not None:
                    information[field] = re.sub(keyword, self.__f, information[field], flags=re.IGNORECASE)
                    foundDF = True
            else:
                for i in information:
                    if re.search(keyword, information[i], flags=re.IGNORECASE) is not None:
                        information[i] = re.sub(keyword, self.__f, information[i], flags=re.IGNORECASE)
                        foundDF = True

            if foundDF:
                results.append(information)

        if len(results) != 0:
            results.sort(key=lambda x: (x["Type"], x["Title"]))

        return results

    def getItems(self):
        """
        Returns all library items sorted by type.

        Returns:
            results (list): A list containing all library items sorted by type. In which:
                results[0]: A list of Book items
                results[1]: A list of CD items
                results[2]: A list of DVD items
                results[3]: A list of Magazine items
        """
        results = [[], [], [], []]

        for item in self.__items:
            res = item.locate()
            if res["Type"] == "Book":
                del res["Type"]
                results[0].append(res)
            elif res["Type"] == "CD":
                del res["Type"]
                results[1].append(res)
            elif res["Type"] == "DVD":
                del res["Type"]
                results[2].append(res)
            elif res["Type"] == "Magazine":
                del res["Type"]
                results[3].append(res)

        for r in results:
            r.sort(key = lambda x: x["Title"])
        return results

    def addItem(self, data):
        """
        Adds new item to library json file.
        
        Parameters:
            data (dict): A dictionary containing information of the item
        """

        self.__data.extend(data)
        updated_json = json.dumps(self.__data, indent=4)

        with open(self.__dataPath, 'w') as file:
            file.write(updated_json)

        self.__update()

    def deleteItems(self, keyword):
        """
        Deletes items that match with keyword by title.

        Parameters:
            keyword (str): keyword to search for
        """
        newData = []
        for i in range(len(self.__data)):
            if keyword not in self.__data[i]["Title"]:
                newData.append(self.__data[i])

        self.__data = newData

        updated_json = json.dumps(self.__data, indent=4)

        with open(self.__dataPath, 'w') as file:
            file.write(updated_json)

        self.__update()


    def __update(self):
        """
        Updates items in the library.
        """
        items = []
        for d in self.__data:
            if d["Type"] == "Book":
                item = Book(d)
            elif d["Type"] == "CD":
                item = CD(d)
            elif d["Type"] == "DVD":
                item = DVD(d)
            else:
                item = Magazine(d)
            items.append(item)
        self.__items = items
            
    def __f(self, match):
        """
        Wraps matched strings with green background.
        """
        return "\x1b[6;30;42m" + match.group(0)[0] + match.group(0)[1:] + "\x1b[0m"


class LibraryItem(ABC):

    """
    An abstract class that contains information about an item in the library.
    The item can be a Book, a CD, a DVD, or a Magazine.
    """
    def __init__(self, data):
        """
        A customized constructor for derived class.

        Parameters:
            data (dict): A dictionary containing information of the item
        """
        self._title = data["Title"]
        self._UPC = data["UPC"]
        self._contributors = []
        for d in data["Contributor"]:
            self._contributors.append(ContributorWithType(d, data["Contributor"][d]))
    
    @abstractmethod
    def locate(self) -> dict:
        """
        An abstract method that locates the item in the library inventory.

        Returns:
            A dictionary containing information of the item.
        """

    def getContribTypes(self):
        """
        Returns a list of contributors' types.
        """
        return [c.getType() for c in self._contributors]

class ContributorWithType:
    """
    A class containing name and type of contributors of a library item.
    """
    def __init__(self, type, contributor):
        """
        Initializes a ContributorWithType object.

        Parameters:
            type (str): Type of contributor (Author, Director, Actor, ...)
            contributor (str): Name of contributors, seperated by ", "
        """
        self.__type = type
        self.__contributor = [Contributor(c) for c in contributor.split(", ")]
    
    def getContributors(self):
        """
        Returns a list containing name of all contributors in the class.
        """
        return [c.getName() for c in self.__contributor]

    def getType(self):
        return self.__type


class Contributor:
    """
    A class containing name of the contributor.
    """
    def __init__(self, name):
        """
        Initializes a Contributor object.

        Parameters:
            name (str): Name of the contributor
        """
        self.__name = name

    def getName(self):
        return self.__name

class Book(LibraryItem):
    """
    A class containing information of book-type item in library.
    """
    def __init__(self, data):
        """
        Initializes a Book object.

        Parameters:
            data (dict): Dictionary of information of the book
        """
        super().__init__(data)
        self.__subject = data["Subject"]
        self.__ISBN = data["ISBN"]
        self.__DDS = data["DDS"]
    def locate(self):
        """
        Overwrites locate method in LibraryItem class.
        """
        contribs = {}
        for c in self._contributors:
            contribs.update({c.getType(): ", ".join(c.getContributors())})

        res = {
            "Title": self._title,
            "Type": "Book"
        }
        res.update(contribs)
        res.update({
            "Subject": self.__subject,
            "ISBN": self.__ISBN,
            "DDS": self.__DDS,
            "UPC": self._UPC
        })

        return res

class CD(LibraryItem):
    """
    A class containing information of CD-type item in library.
    """
    def __init__(self, data):
        """
        Initializes a CD object

        Parameters:
            data (dict): Dictionary of information of the CD
        """
        super().__init__(data)
        self.__genre = data["Genre"]
        self.__ASIN = data["ASIN"]

    def locate(self):
        """
        Overwrites Locate method in LibraryItem class.
        """
        contribs = {}
        for c in self._contributors:
            contribs.update({c.getType(): ", ".join(c.getContributors())})

        res = {
            "Title": self._title,
            "Type": "CD"
        }
        res.update(contribs)
        res.update({
            "Genre": self.__genre,
            "ASIN": self.__ASIN,
            "UPC": self._UPC
        })

        return res

class DVD(LibraryItem):
    """
    A class containing information of DVD-type item in library.
    """
    def __init__(self, data):
        """
        Initializes a DVD object

        Parameters:
            data (dict): Dictionary of information of the DVD
        """
        super().__init__(data)
        self.__genre = data["Genre"]
        self.__ASIN = data["ASIN"]

    def locate(self):
        """
        Overwrites Locate method in LibraryItem class.
        """
        contribs = {}
        for c in self._contributors:
            contribs.update({c.getType(): ", ".join(c.getContributors())})

        res = {
            "Title": self._title,
            "Type": "DVD"
        }
        res.update(contribs)
        res.update({
            "Genre": self.__genre,
            "ASIN": self.__ASIN,
            "UPC": self._UPC
        })

        return res

class Magazine(LibraryItem):
    """
    A class containing information of magazine-type item in library.
    """
    def __init__(self, data):
        """
        Initializes a Magazine object

        Parameters:
            data (dict): Dictionary of information of the magazine
        """
        super().__init__(data)
        self.__volume = data["Volume"]
        self.__issue = data["Issue"]

    def locate(self):
        """
        Overwrites Locate method in LibraryItem class.
        """
        contribs = {}
        for c in self._contributors:
            contribs.update({c.getType(): ", ".join(c.getContributors())})

        res = {
            "Title": self._title,
            "Type": "Magazine",
        }
        res.update(contribs)
        res.update({
            "Volume": self.__volume,
            "Issue": self.__issue,
            "UPC": self._UPC
        })

        return res

