import os
import json
from sys import exit
from catalog import Catalog
from menu import Menu

def addFunc():
    results = []
    res = {}
    count = 0
    while True:
        addMenu = Menu(100, "Add item", "-")
        addMenu.show()
        type = Menu.getKeyLog("Enter item type(Book, CD, DVD, Magazine) or !q to exit")
        if type == "!q":
            break
        if type not in ["Book", "CD", "DVD", "Magazine"]:
            Menu.logError("Wrong type")
            continue
        addMenu.addLines(f"Type: {type}")
        addMenu.show()
        res = {}
        inp = Menu.getKeyLog("Enter title", False)
        res.update({"Title": inp})
        res.update({"Type": type})
        addMenu.addLines(f"Title: {inp}")
        addMenu.show()
        addMenu.addLines("Contributor:")
        contribs = {}
        while True:
            addMenu.show()
            contribType = Menu.getKeyLog("Enter contributor's type (press !q to continue)", False)
            if contribType == "!q":
                if len(contribs)==0:
                    Menu.logError("Must have at least one contributor")
                    continue
                break
            inp = Menu.getKeyLog("Enter contributors' names (seperated by ', ')", False)
            contribs.update({contribType: inp})
            addMenu.addLines(f"    {contribType}: {inp}")
            addMenu.show()
        res.update({"Contributor": contribs})
        if type == "Book":
            inp = Menu.getKeyLog("Enter subject", False)
            res.update({"Subject": inp})
            addMenu.addLines(f"Subject: {inp}")
            addMenu.show()
            inp = Menu.getKeyLog("Enter ISBN", False)
            res.update({"ISBN": inp})
            addMenu.addLines(f"ISBN: {inp}")
            addMenu.show()
            inp = Menu.getKeyLog("Enter DDS", False)
            res.update({"DDS": inp})
            addMenu.addLines(f"ISBN: {inp}")
            addMenu.show()
            inp = Menu.getKeyLog("Enter UPC", False)
            res.update({"UPC": inp})
            addMenu.addLines(f"UPC: {inp}")
            addMenu.show()
        elif type == "CD" or type == "DVD":
            inp = Menu.getKeyLog("Enter genre", False)
            res.update({"Genre": inp})
            addMenu.addLines(f"Genre: {inp}")
            addMenu.show()
            inp = Menu.getKeyLog("Enter ASIN", False)
            res.update({"ASIN": inp})
            addMenu.addLines(f"ASIN: {inp}")
            addMenu.show()
            inp = Menu.getKeyLog("Enter UPC", False)
            res.update({"UPC": inp})
            addMenu.addLines(f"UPC: {inp}")
            addMenu.show()
        else:
            inp = Menu.getKeyLog("Enter volume", False)
            res.update({"Volume": inp})
            addMenu.addLines(f"Volume: {inp}")
            addMenu.show()
            inp = Menu.getKeyLog("Enter issue", False)
            res.update({"Issue": inp})
            addMenu.addLines(f"Issue: {inp}")
            addMenu.show()
            inp = Menu.getKeyLog("Enter UPC", False)
            res.update({"UPC": inp})
            addMenu.addLines(f"UPC: {inp}")
            addMenu.show()
        count += 1
    if res != {}:
        results.append(res)
    addMenu.addLines()
    addMenu.addLines(f"Added {count} items to library.")
    addMenu.show()
    Menu.getKeyLog("Press Enter to continue")
    return results

def main():
    createMenu = Menu(100, "Library Catalog (ver 1.0)")
    createMenu.addLines("A catalog that helps you find what you need in the library.")
    createMenu.addLines()
    createMenu.addList("Create a new Catalog")
    createMenu.addList("Import Catalog from json file")
    createMenu.addList("Quit")

    fileMenu = Menu(100, "Create a new Catalog")

    mainMenu = Menu(100, "Welcome to Library Catalog", "-")
    mainMenu.addList("Search for items with a keyword")
    mainMenu.addList("List all items in the library")
    mainMenu.addList("Add items")
    mainMenu.addList("Delete items")
    mainMenu.addList("Quit")

    searchMenu = Menu(100, "Search for items with a keyword", "-")
    searchMenu.addList("Search by title")
    searchMenu.addList("Search by contributors")
    searchMenu.addList("Search by UPC")
    searchMenu.addList("Quit")

    searchByMenu = Menu(100, sep="-")



    fileName = ""
    while True:
        createMenu.show()
        choice = Menu.getChoice(3)
        if choice == -1:
            Menu.logError("Invalid value.")
            continue
        if choice == 1:
            fileMenu.show()
            fileName = fileMenu.getKeyLog("Enter file name")
            fileName = fileName if ".json" in fileName else fileName + ".json"
            if os.path.isfile(fileName):
                choice = Menu.getKeyLog("File exists. Doing this will delete all content of the file. Continue? (y/n)")
                if choice.lower() != "y":
                    Menu.clear()
                    Menu.getKeyLog("Aborted. Press Enter to continue")
                    continue
            res = []
            while True:
                res = addFunc()
                if len(res) == 0:
                    Menu.logError("You have to add at least 1 item to the library.")
                    continue
                break
            data = json.dumps(res, indent=4)
            with open(fileName, "w") as newFile:
                newFile.write(data)
            ctl = Catalog(fileName)
        elif choice == 2:
            fileMenu.setTitle("Import Catalog from json file")
            fileMenu.show()
            fileName = fileMenu.getKeyLog("Enter file name")
            fileName = fileName if ".json" in fileName else fileName + ".json"
            if not os.path.isfile(fileName):
                Menu.logError("File not found.")
                continue
        elif choice == 3:
            Menu.clear()
            exit()
        break

    while True:
        ctl = Catalog(fileName)
        mainMenu.show()
        choice = Menu.getChoice(5)
        if choice == -1:
            Menu.logError("Invalid value")
        if choice == 1:
            while True:
                resultMenu = Menu(100, sep="-")
                searchMenu.show()
                choice = Menu.getChoice(4)
                if choice == -1:
                    Menu.logError("Invalid value")
                    continue
                if choice == 1:
                    searchByMenu.setTitle("Search by title")
                    searchByMenu.show()
                    res = ctl.search(Menu.getKeyLog("Enter a keyword"), "Title")
                    resultMenu.setTitle("Found " + str(len(res)) + " items")
                    resultMenu.addLines(Catalog.convert(res))
                    resultMenu.show()
                    Menu.getKeyLog("Press Enter to continue")
                elif choice == 2:
                    searchByMenu.setTitle("Search by contributors")
                    searchByMenu.show()
                    res = ctl.search(Menu.getKeyLog("Enter a keyword"), "Contributor")
                    resultMenu.setTitle("Found " + str(len(res)) + " items")
                    resultMenu.addLines(Catalog.convert(res))
                    resultMenu.show()
                    Menu.getKeyLog("Press Enter to continue")
                elif choice == 3:
                    searchByMenu.setTitle("Search by UPC")
                    searchByMenu.show()
                    res = ctl.search(Menu.getKeyLog("Enter a keyword"), "UPC")
                    resultMenu.setTitle("Found " + str(len(res)) + " items")
                    resultMenu.addLines(Catalog.convert(res))
                    resultMenu.show()
                    Menu.getKeyLog("Press Enter to continue")
                else:
                    break

        elif choice == 2:
            res = ctl.getItems()
            menus = [Menu(100, "Book: "+str(len(res[0]))+" items", "-"), Menu(100, "CD: "+str(len(res[1]))+" items", "-"), Menu(100, "DVD: "+str(len(res[2]))+" items", "-"), Menu(100, "Magazine: "+str(len(res[3]))+" items", "-")]
            for i, menu in enumerate(menus):
                menu.addLines(Catalog.convert(res[i]))
                menu.show()
                Menu.getKeyLog("Press Enter to continue")
        elif choice == 3:
            res = addFunc()
            ctl.addItem(res)
        elif choice == 4:
            deleteMenu = Menu(100, "Delete item", "-")
            deleteMenu.show()
            keyword = Menu.getKeyLog("Enter the title of the item you want to delete")
            matches = ctl.search(keyword, "Title")
            delItems = len(matches)
            matches = Catalog.convert(matches)
            if matches == "":
                deleteMenu.addLines("Found 0 items...")
                deleteMenu.show()
                Menu.getKeyLog("Press Enter to continue")
                continue
            deleteMenu.addLines(matches)
            deleteMenu.show()
            choice = Menu.getKeyLog("Are you sure you want to delete these items? (y/n)")
            if choice.lower() == "y":
                ctl.deleteItems(keyword)
                deleteMenu.addLines(f"Delete {delItems} items.")
                deleteMenu.show()
                Menu.getKeyLog("Press Enter to continue")
            else:
                Menu.getKeyLog("Aborted. Press Enter to continue")
        elif choice == 5:
            Menu.clear()
            exit()

if __name__ == "__main__":
    main()
