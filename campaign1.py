
from curses import wrapper
from main import Inventory,Location,BasicLocker,LockedLocker,Resource,Room,WorkBench
from IO import SCREENMANAGER

@wrapper
def main(stdscr):
    screenmanager = SCREENMANAGER(stdscr)
    inventory = Inventory({"Pickaxe":50})
    chest1 = BasicLocker("Chest","You open the old looking chest",((1,"Gold",False),(3,"Silver",False),(1,"Key",False)))
    chest2 = LockedLocker("Chest","You try to unlock the old looking chest",((1,"Gold",False),(3,"Silver",False)),(1,"Key",False),"You open the chest discovering the loot hidden inside")
    crafter = WorkBench("Bench")
    ironnode = Resource("Iron node","You mine through the iron node",[[1,"Iron",False]],"Pickaxe",50)
    goldnode = Resource("Gold node","You mine through the gold node",[[1,"Gold",False]],"Pickaxe",60)
    room1 = Room("Caverns1","You enter a digy lit cavern. You can see a rusted old chest in front of you",[],[ironnode,ironnode,goldnode,crafter],[chest1],right="continue right")
    room2 = Room("Caverns2","You enter a digy lit cavern. You can see a locked chest in front of you",[],[goldnode],[chest2],left="continue left")
    location1 = Location("Deep caverns",{(3,3):room1,(3,4):room2},[3,3])
    location1.runLocation(inventory,screenmanager)