
from curses import wrapper
from main import Inventory,Location,BasicLocker,LockedLocker,Resource,WorkBench,Room
from IO import SCREENMANAGER

@wrapper
def main(stdscr):
    screenmanager = SCREENMANAGER(stdscr)
    inventory = Inventory({
        "Pickaxe":50,
        "Sickle" : 50,
        })
    
    '''
    Reasource node setup
    '''
    ironnode1 = Resource("Iron node","You mine through the iron node",[[1,"Iron ore",False]],"Pickaxe",50)
    ironnode2 = Resource("Iron node","You mine through the iron node",[[2,"Iron ore",False]],"Pickaxe",50)
    ironnode3 = Resource("Iron node","You mine through the iron node",[[3,"Iron ore",False]],"Pickaxe",50)

    goldnode1 = Resource("Gold node","You mine through the Gold node",[[1,"Gold ore",False]],"Pickaxe",60)
    goldnode2 = Resource("Gold node","You mine through the Gold node",[[2,"Gold ore",False]],"Pickaxe",60)
    goldnode3 = Resource("Gold node","You mine through the Gold node",[[3,"Gold ore",False]],"Pickaxe",60)

    mushroom1 = Resource("Mushrooms","You gather the mushrooms",[[1,"Mushroom",False]],"Sickle",30)
    mushroom2 = Resource("Mushrooms","You gather the mushrooms",[[2,"Mushroom",False]],"Sickle",30)
    mushroom3 = Resource("Mushrooms","You gather the mushrooms",[[3,"Mushroom",False]],"Sickle",30)


    '''
    Locker setup
    '''
    chest1 = BasicLocker("Chest","You open the rusty old chest",[[1,"Gold",False],[3,"Iron ore",False]])
    chest2 = BasicLocker("Chest","You open the golden chest",[[3,"Gold",False],[7,"Iron ore",False]])
    chest3 = LockedLocker("Grand Chest","You try to open the chest but notice a lock",[[10,"Gold",False],[30,"Silver",False]],[1,"Grand key",False],"Using the grand key you open the chest revealing many lost treasures")

    rubble1 = BasicLocker("Pile of rubble","You sift through the rubble seeing if you can find anything",[[1,"Grand key",False]])
    rubble2 = BasicLocker("Pile of rubble","After sifting through the rubble for a while you cannot find anything",[])
    rubble3 = BasicLocker("Pile of rubble","You spend some time going through the mound of rocks and dust finding a few ores worth keeping",[[2,"Iron ore",False],[2,"Gold ore",False]])
    rubble4 = BasicLocker("Pile of rubble","Rumaging around through the rock, dust and muck you uncover a hidden gem. What great luck!",[[1,"Diamond",False]])

    crate1 = BasicLocker("Mining Crate","Looking through the rotting crate you find a variety of old mining gear",[[1,"Miners Helmet",False],[1,"Dynamite",False]])
    crate2 = BasicLocker("Mining Crate","Looking through the slowly crumbling crate you find nothing of worth",[])
    crate3 = BasicLocker("Mining Crate","Searching thought the crate you find some explosives",[[1,"Dynamite",False]])

    hivenest = LockedLocker("Hive Nest","This ugly lump of pulsating flesh and rock will need to be disposed of",[[3,"Hive flesh",False],[1,"HiveClearedFlag",True]],[1,"Dynamite",False],"After setting up the dynamite you run away, returning after hearing a large bang to a charred mound of rosted Hive")

    '''
    Crafter setup
    '''

    crafter = WorkBench("Work bench")

    '''
    Room setup
    '''
    enterance1 = Room("Enterance 1","Light streams from outside into the opening in the rock",[],[],[],left="Continue deeper")
    enterance2 = Room("Enterance 2","There is a low glow of sunlight which still reaches into the cave however the path ahead seems to only get darker",[],[mushroom2],[rubble3,rubble2],right="Return to the enterance",down="Push deeper")
    enterance3 = Room("Enterance 3","Before you is a long strenching hallway lit by flickering candles",[],[mushroom1,mushroom3],[],up="Return to the enterance",left="Push deeper")
    enterance4 = Room("Enterance 4","Coming up on an opening you spot a few scattered tools next to some old mining crates",[],[],[crate1],right="Return to the enterance",down="Push deeper")
    enterance5 = Room("Enterance 5","You coninue down a winding mineshaft noticing some ores which had not yet been mined",[],[ironnode2,ironnode1],[],up="Return to the enterance",down="Push deeper")

    crossroads = Room("The crossroads","You enter a wide carvern space which was clearly used as a base of operations for the miners. There is rubble and tools scattered around aswell as a rapidly deteriorating workbench.",[],[ironnode1],[rubble1,rubble2,crafter],up="Return to the enterance",left="Take the left path",down="Go deeper")

    caverns1 = Room("Caverns 1","The as you walk down the corridor the gradient of darker rock deeper in the caverns becomes clear. You occasionally pass the odd box or pile of rubble however there is not much of note.",[],[],[crate3],left="Explore the caverns further",right="Return to the crossroads")
    caverns2 = Room("Caverns 2","You come to an opening where it is clear heavy excuvation has occured.",[],[ironnode1,ironnode2,goldnode2,goldnode3],[],right="Return to the crossroads",down="Explore the caverns further")
    caverns3 = Room("Caverns 3","Finally coming to the end of the winding corridoors you find a horrific lump of pulsing flesh and rubble and dust. A horrid scent of dissolving bones reached your nostrils.",[],[],[hivenest],up="Return to the crossroads")

    deepcaverns1 = Room("Deep Caverns 1","",[],[goldnode2,goldnode1,ironnode1],[],up="Return to the crossroads",right="Explore deeper into the deep caverns")
    deepcaverns2 = Room("Deep Caverns 2","",[],[],[hivenest],left="Return to the crossroads",down="Explore deeper into the deep caverns")
    deepcaverns3 = Room("Deep Caverns 3","",[],[ironnode1,ironnode1,ironnode2],[],up="Return to the crossroads",right="Go Right",left="Go Left")
    deepcaverns4 = Room("Deep Caverns 4","",[],[],[crate3,chest3],left="Return to the crossroads")
    deepcaverns5 = Room("Deep Caverns 5","",[],[],[hivenest],right="Return to the crossroads")

    world = Location("The caves",{
        (0,4) : enterance1, (0,3) : enterance2, (1,3) : enterance3, (1,2) : enterance4, (2,2) : enterance5,
        (3,2) : crossroads,
        (3,1) : caverns1, (3,0) : caverns2, (4,0) : caverns3,
        (4,2) : deepcaverns1, (4,3) : deepcaverns2, (5,3) : deepcaverns3, (5,4) : deepcaverns4, (5,2) : deepcaverns5
    },
    [0,4])
    world.runLocation(inventory,screenmanager)