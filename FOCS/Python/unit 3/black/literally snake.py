import random
import time


cord = {(0, 0): {'seen': 0, 'place': False, 'tent': False, 'mud': False, 'die': False}, (1, 0): {'seen': 0, 'place': False, 'tent': False, 'mud': False, 'die': False}, (2, 0): {'seen': 0, 'place': False, 'tent': False, 'mud': False, 'die': False}, (3, 0): {'seen': 0, 'place': False, 'tent': False, 'mud': False, 'die': False}, (4, 0): {'seen': 0, 'place': False, 'tent': False, 'mud': False, 'die': False}, (5, 0): {'seen': 0, 'place': False, 'tent': False, 'mud': False, 'die': False}, (6, 0): {'seen': 0, 'place': False, 'tent': False, 'mud': False, 'die': False}, (0, 1): {'seen': 0, 'place': False, 'tent': False, 'mud': False, 'die': False}, (1, 1): {'seen': 0, 'place': False, 'tent': False, 'mud': False, 'die': False}, (2, 1): {'seen': 0, 'place': False, 'tent': False, 'mud': False, 'die': False}, (3, 1): {'seen': 0, 'place': False, 'tent': False, 'mud': False, 'die': False}, (4, 1): {'seen': 0, 'place': False, 'tent': False, 'mud': False, 'die': False}, (5, 1): {'seen': 0, 'place': False, 'tent': False, 'mud': False, 'die': False}, (6, 1): {'seen': 0, 'place': False, 'tent': False, 'mud': False, 'die': False}, (0, 2): {'seen': 0, 'place': False, 'tent': False, 'mud': False, 'die': False}, (1, 2): {'seen': 0, 'place': False, 'tent': False, 'mud': False, 'die': False}, (2, 2): {'seen': 0, 'place': False, 'tent': False, 'mud': False, 'die': False}, (3, 2): {'seen': 0, 'place': False, 'tent': False, 'mud': False, 'die': False}, (4, 2): {'seen': 0, 'place': False, 'tent': False, 'mud': False, 'die': False}, (5, 2): {'seen': 0, 'place': False, 'tent': False, 'mud': False, 'die': False}, (6, 2): {'seen': 0, 'place': False, 'tent': False, 'mud': False, 'die': False}, (0, 3): {'seen': 0, 'place': False, 'tent': False, 'mud': False, 'die': False}, (1, 3): {'seen': 0, 'place': False, 'tent': False, 'mud': False, 'die': False}, (2, 3): {'seen': 0, 'place': False, 'tent': False, 'mud': False, 'die': False}, (3, 3): {'seen': 0, 'place': False, 'tent': False, 'mud': False, 'die': False}, (4, 3): {'seen': 0, 'place': False, 'tent': False, 'mud': False, 'die': False}, (5, 3): {'seen': 0, 'place': False, 'tent': False, 'mud': False, 'die': False}, (6, 3): {'seen': 0, 'place': False, 'tent': False, 'mud': False, 'die': False}, (0, 4): {'seen': 0, 'place': False, 'tent': False, 'mud': False, 'die': False}, (1, 4): {'seen': 0, 'place': False, 'tent': False, 'mud': False, 'die': False}, (2, 4): {'seen': 0, 'place': False, 'tent': False, 'mud': False, 'die': False}, (3, 4): {'seen': 0, 'place': False, 'tent': False, 'mud': False, 'die': False}, (4, 4): {'seen': 0, 'place': False, 'tent': False, 'mud': False, 'die': False}, (5, 4): {'seen': 0, 'place': False, 'tent': False, 'mud': False, 'die': False}, (6, 4): {'seen': 0, 'place': False, 'tent': False, 'mud': False, 'die': False}, (0, 5): {'seen': 0, 'place': False, 'tent': False, 'mud': False, 'die': False}, (1, 5): {'seen': 0, 'place': False, 'tent': False, 'mud': False, 'die': False}, (2, 5): {'seen': 0, 'place': False, 'tent': False, 'mud': False, 'die': False}, (3, 5): {'seen': 0, 'place': False, 'tent': False, 'mud': False, 'die': False}, (4, 5): {'seen': 0, 'place': False, 'tent': False, 'mud': False, 'die': False}, (5, 5): {'seen': 0, 'place': False, 'tent': False, 'mud': False, 'die': False}, (6, 5): {'seen': 0, 'place': False, 'tent': False, 'mud': False, 'die': False}, (0, 6): {'seen': 0, 'place': False, 'tent': False, 'mud': False, 'die': False}, (1, 6): {'seen': 0, 'place': False, 'tent': False, 'mud': False, 'die': False}, (2, 6): {'seen': 0, 'place': False, 'tent': False, 'mud': False, 'die': False}, (3, 6): {'seen': 0, 'place': False, 'tent': False, 'mud': False, 'die': False}, (4, 6): {'seen': 0, 'place': False, 'tent': False, 'mud': False, 'die': False}, (5, 6): {'seen': 0, 'place': False, 'tent': False, 'mud': False, 'die': False}, (6, 6): {'seen': 0, 'place': False, 'tent': False, 'mud': False, 'die': False}}

def maker(size,nested={}):
    for i in [(x, y) for y in range(size) for x in range(size)]:
        nested[i]={"seen": 0, "place": False,"tent": False, "mud": False, "die": False}
    return nested


def hazards(coord, difficulty=1, test=False): 
    num = list(coord.copy())
    
    die=random.choice(num) 
    num.remove(die)
    
    tent = []
    mud = []
    
    tent1=random.choice(num)
    tent.append(tent1), num.remove(tent1)
    
    mud1 = random.choice(num) 
    mud.append(mud1),num.remove(mud1)
       
    if difficulty == 2:
        tent2=random.choice(num)
        tent.append(tent2), num.remove(tent2)
        
        mud2=random.choice(num)
        mud.append(mud2), num.remove(mud2)
    
    for i in tent:
        coord[i]["tent"]=True
    
    for i in mud:
        coord[i]["mud"]=True
    
    if test:
        print("Tent:",tent)
        print("Mud:",mud)
        print("Die:",die)
        print()
        print(coord)
    
    else:
        return coord


def printer(coord,size,x=0):
    lst=[]
    
    for i in [(x, y) for y in range(size) for x in range(size)]:
        if coord[i]["place"]:
            lst.append("O")
            
        elif coord[i]["seen"]==0:
            lst.append(" ")
        
        elif coord[i]["seen"]>0 and not coord[i]["tent"] and not coord[i]["mud"] and not coord[i]["die"]:
            lst.append(".")
        
        elif coord[i]["seen"]==1 and coord[i]["tent"] and not coord[i]["mud"] and not coord[i]["die"]:
            lst.append("~")
            
        elif coord[i]["seen"]==1 and coord[i]["mud"]:
            lst.append("X")
        
        elif coord[i]["seen"]==1 and coord[i]["die"]:
            lst.append("X")
        
        elif coord[i]["seen"]==2 and coord[i]["tent"]:
            lst.append("X")
            
    horizontal = "     "     
    bar="-"*(4*(size)+1)
    for i in range(size):
        horizontal+= str(i)+"   "
    print(horizontal+"\n   "+bar)
    for i in range(size,size**2,size):
        print(x," | " + " | ".join(lst[i-size:i]) + " |" +"\n")
        x+=1
    print(x, " | " + " | ".join(lst[(size**2)-size:]) + " |")
    print("   "+bar)



def move(coord, size):
    num=list(coord.copy())
    pos=random.choice(num)
    coord[pos]["place"]=True
    arrows=2
    
    printer(coord,size)
    print("\n" + "You are at position:",pos)    
    print("Arrows:",arrows)
    
    alive=True
    fill="-"*64
    
    while alive:
        inp=input("Where do you want to move? ").lower()
        
        coord[pos]["place"]=True
        
        tmp = list(pos)
        x=tmp[0]
        y=tmp[1]
        
        if inp=="q":
            print("\n"+fill+"\nDid you really think you could escape Shrek's Swamp that easily?\n\nNo no, you shall not leave.\n"+fill)
        
        elif inp not in "wasdq":
            print("\n"+fill+"----\nThat is not a valid move.\n\nRemember: 'W' for up, 'A' for left, 'S' for down, and 'D' for right.\n"+fill+"----")
            
        elif inp == "w":
            pos=(x,(y-1)%size)
            coord[pos]["seen"]+=1
            print(pos)
            
        elif inp == "a":
            pos=((x-1)%size,y)
            coord[pos]["seen"]+=1
            print(pos)
            
        elif inp == "s":
            pos=(x,(y+1)%size)
            coord[pos]["seen"]+=1
            print(pos)
            
        elif inp == "d":
            pos=((x+1)%size,y)
            coord[pos]["seen"]+=1
            print(pos)
        
        print()
        printer(coord,size)

size=10
move(hazards(maker(size)),size)