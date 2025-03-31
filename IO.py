
import curses 
from curses import wrapper


def logger(item):
    global lines
    with open("log.txt", "a") as handle:
        if type(item) == str:
            handle.writelines(item)
        elif type(item) == int:
            handle.writelines(str(item))
        elif type(item) == list[list]:
            newlist = []
            for y in list:
                newelement = ""
                for x in list:
                    newelement += str(item[y][x])
                newlist.append(newelement)
            for element in newelement:
                handle.writelines(str(element) + "\n")
        elif type(item) == list:
            for element in item:
                handle.writelines(str(element) + "\n")

class LOCATIONSWINDOW:

    def __init__(self,dy,dx,y,x,stdscr):
        self.window = curses.newwin(dy,dx,y,x)
        stdscr.refresh()
        self.window.border()
        self.window.refresh()
        self.places = []
        pass

    def update(self):
        string = ""
        for place in self.places:
            string += place + " - "
        string = string[:-3]
        self.window.addstr(1,1,string)
        self.window.refresh()

    def enter(self,location):
        self.places.append(location)
        self.update()

    def exit(self):
        self.places.pop()
        self.update()


class TEXTWINDOW:

    def __init__(self,dy,dx,y,x,stdscr):
        self.window = curses.newwin(dy,dx,y,x)
        stdscr.refresh()
        self.window.border()
        self.window.refresh()
        self.queue = []
        pass

    def addText(self,sentence,newline=False):
        words = sentence.split()
        length = 0
        string = ""
        for word in words:
            length = len(string) + len(word)
            if length > self.window.getmaxyx()[1] - 2:
                self.queue.append(string)
                string = ""
                length = len(word) + 1
            string += word + " "
        self.queue.append(string)

        if newline:
            self.queue.append(" ")
        
        if len(self.queue) - 1 > self.window.getmaxyx()[0] - 2:
            self.queue = self.queue[-5:]
        self.window.clear()
        for i in range(len(self.queue)):
            self.window.addstr(i +1,1 ,self.queue[i])
        self.window.border()
        self.window.refresh()

class OPTIONSWINDOW:

    def __init__(self,dy,dx,y,x,stdscr):
        self.window = curses.newwin(dy,dx,y,x)
        self.stdscr = stdscr
        stdscr.refresh()
        self.window.border()
        self.window.refresh()
        pass

    def addOptions(self,options):
        self.window.clear()
        self.window.border()
        self.window.refresh()
        pointer = 0
        while True:
            for i in range(len(options)):
                if i == pointer:
                    self.window.addstr(i+1,1,options[i],curses.A_REVERSE)
                else:
                    self.window.addstr(i+1,1,options[i])
            self.window.border()
            self.window.refresh()
            key = self.stdscr.getkey()
            if key == "KEY_DOWN":
                pointer += 1
                if pointer > len(options) - 1:
                    pointer = 0
            if key == "KEY_UP":
                pointer -= 1
                if pointer < 0:
                    pointer = len(options) -1
            if key == "\n":
                return pointer

class MAPWINDOW:

    def __init__(self,dy,dx,y,x,stdscr):
        self.window = curses.newwin(dy,dx,y,x)
        self.stdscr = stdscr
        stdscr.refresh()
        self.window.border()
        self.window.refresh()
        pass

    def addMap(self,map):
        y , x = self.window.getmaxyx()
        centery = y//2
        centerx = x//2
        rows = len(map)
        for y in range(rows):
            cols = len(map[y])
            for x in range(cols):
                self.window.addstr(centery - rows//2 + y,centerx - cols//2 + x,map[y][x])
        self.window.refresh()

class SCREENMANAGER:

    def __init__(self,stdscr):
        self.locationwindow = LOCATIONSWINDOW(3,175,0,0,stdscr)
        self.storywindow = TEXTWINDOW(37,131,2,0,stdscr)
        self.mapwindow = MAPWINDOW(37,44,2,131,stdscr)
        self.optionswindow = OPTIONSWINDOW(15,106,39,0,stdscr)
        self.inventorywindow = TEXTWINDOW(15,69,39,106,stdscr)
        pass

    def enterLocation(self,location):
        self.locationwindow.enter(location)
    
    def exitLocation(self):
        self.locationwindow.exit()

    def addStory(self,text):
        self.storywindow.addText(text,True)
    
    def addInventory(self,text):
        self.inventorywindow.addText(text)
    
    def makeDecision(self,options):
        return self.optionswindow.addOptions(options)
    
    def updateMap(self,map):
        self.mapwindow.addMap(map)
'''
@wrapper
def MAIN(stdscr:curses.window):
    screenmanager = SCREENMANAGER(stdscr)
    screenmanager.addStory("You enter a cold dark cave")
    screenmanager.addStory("You open a chest")
    screenmanager.addInventory("-1 key")
    screenmanager.addInventory("+1 gold")
    screenmanager.addInventory("+3 silver")
    screenmanager.enterLocation("house")
    stdscr.getkey()
    pass

if __name__ == "__main__":
    MAIN()
'''