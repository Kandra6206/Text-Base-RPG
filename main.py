
from dataclasses import dataclass
from copy import deepcopy
from IO import logger

class Inventory:

    def __init__(self,tools):
        self.items = { "Iron" : 50}
        self.hiddenitems = {}
        self.tools = tools

    def upgradeTool(self,screenmanager):
        options = []
        for tool in self.tools:
            options.append(f"{tool} [-{self.tools[tool]//10} Iron]")

        toolref = screenmanager.makeDecision(options)

        tool = options[toolref].split(" ")[0]
        if self.findItem([0,"Iron",False]) >= self.tools[tool]//10:
            self.removeItem(screenmanager,[self.tools[tool]//10,"Iron",False])
            self.tools[tool] += 10
            screenmanager.addInventory(f"+10 Power [{tool}]")
        pass
    
    def findItem(self,item):
        if item[2]:
            return self.hiddenitems.get(item[1],0)
        return self.items.get(item[1],0)
    
    def addItem(self,screenmanager,item):
        itemtype = self.hiddenitems
        if not item[2]:
            itemtype = self.items
            screenmanager.addInventory(f"+{item[0]} {item[1]}")
        if not itemtype.get(item[0]):
            itemtype[item[1]] = 0
        itemtype[item[1]] += item[0]
    
    def removeItem(self,screenmanager,item):
        if self.findItem(item) >= item[0]:
            itemtype = self.hiddenitems
            if not item[2]:
                itemtype = self.items
                screenmanager.addInventory(f"-{item[0]} {item[1]}")
            itemtype[item[1]] -= item[0]
            return True
        return False

class Puzzle:

    def __init__(self):
        pass

class Locker:

    def __init__(self,name,desc,items):
        self.name = name
        self.desc = desc
        self.items = items
        pass

    def run(self,inventory,screenmanager):        
        for item in self.items:
            inventory.addItem(screenmanager,item)
        return True 

class BasicLocker(Locker):

    def __init__(self, name, desc, items):
        super().__init__(name, desc, items)

    def run(self,inventory,screenmanager):
        screenmanager.addStory(self.desc)
        return super().run(inventory,screenmanager)

class LockedLocker(Locker):

    def __init__(self, name, desc, items, key, opendesc):
        super().__init__(name, desc, items)
        self.key = key
        self.opendesc = opendesc
    
    def run(self,inventory,screenmanager):
        screenmanager.addStory(self.desc)
        if not inventory.removeItem(screenmanager,self.key):
            return False
        screenmanager.addStory(self.opendesc)
        return super().run(inventory,screenmanager)

class PuzzleLocker(Locker):

    def __init__(self, name, desc, items, puzzle, opendesc):
        super().__init__(name, desc, items)
        self.puzzle = puzzle
        self.opendesc = opendesc
    
    def run(self,inventory,screenmanager):
        screenmanager.addStory(self.desc)
        if not self.puzzle.run():
            return False
        screenmanager.addStory(self.opendesc)
        return super().run(inventory,screenmanager)
    
class Resource:

    def __init__(self,name,desc,items,tool,toolpower):
        self.name = name
        self.desc = desc
        self.items = items
        self.tool = tool
        self.toolpower = toolpower
        pass

    def run(self,inventory,screenmanager):
        if self.toolpower > inventory.tools[self.tool]:
            screenmanager.addStory(f"Your {self.tool} is not powerful enough [{inventory.tools[self.tool]}/{self.toolpower}]")
            return False
        screenmanager.addStory(self.desc)
        for item in self.items:
            inventory.addItem(screenmanager,item)
        return True

class WorkBench:

    def __init__(self,name):
        self.name = name
        pass

    def run(self,inventory,screenmanager):
        inventory.upgradeTool(screenmanager)
        pass

class Room:

    def __init__(self,name,desc,enteritems,resources,lockers,up = None,down = None,left = None,right = None):
        self.discovered = False
        self.name = name
        self.desc = desc
        self.enteritems = enteritems
        self.lockers = lockers
        self.resources = resources
        self.exits = [up,down,left,right]
        self.visual = self.formVisual()
        pass

    def formVisual(self):
        array = [[" " for i in range(5)] for j in range(5)]
        blocks = [(1,1),(3,1),(1,3),(3,3)]
        exits = (((0,1),(0,3),(1,2)),((4,1),(4,3),(3,2)),((1,0),(3,0),(2,1)),((1,4),(3,4),(2,3)))
        for i in range(4):
            if self.exits[i]:
                blocks.append(exits[i][0])
                blocks.append(exits[i][1])
            else:
                blocks.append(exits[i][2])
        for block in blocks:
            array[block[0]][block[1]] = "█"
        return array

    def enterRoom(self,entering,inventory,screenmanager):
        
        if entering:
            screenmanager.addStory(self.desc)

        if self.enteritems:
            for item in self.enteritems:
                inventory.addItem(item)
            self.enteritems = []
        
        options = []
        lockernum = 0
        for locker in self.lockers:
            lockernum += 1
            option = locker.name
            if type(locker) == LockedLocker:
                option += f" [-{locker.key[0]} {locker.key[1]}]"
            options.append(option)
        resourcenum = 0
        for resource in self.resources:
            resourcenum += 1
            options.append(resource.name)
        exitnum = 0
        for exit in self.exits:
            if exit != None:
                exitnum += 1
                options.append(exit)
        options.append("Quit")

        choice = screenmanager.makeDecision(options)

        if choice < lockernum:
            if self.lockers[choice].run(inventory,screenmanager):
                self.lockers.pop(choice)
        elif choice < lockernum + resourcenum:
            if self.resources[choice-lockernum].run(inventory,screenmanager):
                self.resources.pop(choice-lockernum)
        elif choice < lockernum + resourcenum + exitnum:
            exit = self.exits.index(options[choice])
            moves = ((-1,0),(1,0),(0,-1),(0,1))
            return moves[exit]
        else:
            return "Quit"
        
        return (0,0)

class Location:

    def __init__(self,name,rooms,startroom):
        self.name = name
        self.rooms = rooms
        self.currentroom = startroom
        self.lastroom = (-1,-1)
        self.map = self.makeMap()
    
    def runLocation(self,inventory,screenmanager):
        action = ""
        self.lastroom = (-1,-1)
        screenmanager.enterLocation(self.name)
        screenmanager.enterLocation("")
        while True:
            self.rooms[tuple(self.currentroom)].discovered = True
            self.map = self.makeMap()
            screenmanager.updateMap(self.map)
            if self.lastroom == self.currentroom:
                action = self.rooms[tuple(self.currentroom)].enterRoom(False,inventory,screenmanager)
            else:
                screenmanager.exitLocation()
                screenmanager.enterLocation(self.rooms[tuple(self.currentroom)].name)
                action = self.rooms[tuple(self.currentroom)].enterRoom(True,inventory,screenmanager)
            if action == "Quit":
                break
            self.lastroom = deepcopy(self.currentroom)
            self.currentroom[0] += action[0]
            self.currentroom[1] += action[1]
            pass

    def makeMap(self):
        array = [[" " for i in range(35)] for i in range(35)]
        addedarrays = []
        for pos in self.rooms:
            if self.rooms[pos].discovered:
                addedarrays.append((pos,self.rooms[pos].visual))
        for pos,addarray in addedarrays:
            startpos = (pos[0]*5,pos[1]*5)
            for y in range(5):
                for x in range(5):
                    array[startpos[0]+y][startpos[1]+x] = addarray[y][x]
        array[(self.currentroom[0]*5)+2][(self.currentroom[1]*5)+2] = "x"
        return array



