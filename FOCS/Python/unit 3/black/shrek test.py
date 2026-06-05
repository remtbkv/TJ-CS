import random

def maker(size,nested={}):
    for i in [(x, y) for y in range(size) for x in range(size)]:
        nested[i]={"seen": 0, "place": False,"tent": False, "mud": False, "shrek": False, "arrow": False, "tnear": False, "mnear": False, "snear": False}
    return nested

# def near(list):


def hazards(coord, difficulty=1, test=True): 
    num = list(coord.copy())
    
    shrek=random.choice(num) 
    coord[shrek]["shrek"]=True
    # coord[]["snear"]=True
    
    num.remove(shrek)
    
    
    
    aro=random.choice(num)
    coord[aro]["arrow"]=True
    num.remove(aro)
    
    pos=random.choice(num)
    coord[pos]["place"]=True
    coord[pos]["seen"]+=1
    num.remove(pos)
        
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
        i=list(i)
        # coord[]["tnear"]=True
    
    for i in mud:
        coord[i]["mud"]=True
        i=list(i)
        # coord[]["mnear"]=True
        
    if test:
        print("Tent:",tent)
        print("Mud:",mud)
        print("Shrek:",shrek)
        print("Arrow:",aro)
        print()
        # print(coord)
    
    return coord


def printer(coord,size,x=0,z=0):
    lst=[]
    coordinates=[(x, y) for y in range(size) for x in range(size)]
    while z<size**2:
        i=coordinates[z]
        
        if coord[i]["seen"]==0 and not coord[i]["place"]:
            lst.append(" ")
        
        elif coord[i]["place"] and not coord[i]["tent"] and not coord[i]["mud"] and not coord[i]["shrek"]:
            lst.append("O")
        
        elif coord[i]["seen"]>0 and not coord[i]["tent"] and not coord[i]["mud"] and not coord[i]["shrek"]:
            lst.append(".")
        
        elif coord[i]["seen"]==1 and coord[i]["tent"] and not coord[i]["shrek"]:
            lst.append("~")
            
        elif coord[i]["seen"]==1 and coord[i]["mud"] or coord[i]["shrek"]:
            lst.append("X")
        
        elif coord[i]["seen"]==2 and coord[i]["tent"]:
            lst.append("X")
    
        z+=1
    
            
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


def updater(aro=0, moved=False, leave=False,wrong=False):
    fill = "-"*68
    if moved:
        print("\n"+fill+"\nThe tentacles have transported you to a different location!\n"+fill)
    elif leave:
        print("\n"+fill+"\nDid you really think you could escape Shrek's Swamp that easily?\n\nNo no, you shall not leave.\n"+fill)
    elif wrong:
        print("\n"+fill+"\nThat is not a valid move.\n\nRemember: 'W' for up, 'A' for left, 'S' for down, and 'D' for right.\n"+fill)
    elif aro==1:
        print("\n"+fill+"\nYou have acquired an arrow. Go shoot Shrek with it!\n"+fill)
        

def move(coord, size, alive=True, aro=0, moved=False, leave=False,wrong=False):
    for i in coord:
        if coord[i]["place"]:
            pos=i
        
    while alive:
        
        printer(coord,size)
        print("\nYou are at position:",pos)
        updater(aro, moved, leave, wrong)
        coord[pos]["place"]=False
        moved=False
        leave=False
        wrong=False
        if aro==1:
            aro+=1
        
        inp=input("Where do you want to move? ").lower()
        
        tmp = list(pos)
        x=tmp[0]
        y=tmp[1]
        
        if inp=="q":
            leave=True
        
        elif inp not in "wasd":
            wrong=True
            
        elif inp == "w":
            pos=(x,(y-1)%size)
            coord[pos]["seen"]+=1
            coord[pos]["place"]=True
            
        elif inp == "a":
            pos=((x-1)%size,y)
            coord[pos]["seen"]+=1
            coord[pos]["place"]=True
            
        elif inp == "s":
            pos=(x,(y+1)%size)
            coord[pos]["seen"]+=1
            coord[pos]["place"]=True
            
        elif inp == "d":
            pos=((x+1)%size,y)
            coord[pos]["seen"]+=1
            coord[pos]["place"]=True
            
        print()
        
        if coord[pos]["mud"] or coord[pos]["shrek"]:
            alive=False
        
        elif coord[pos]["seen"]==2 and coord[pos]["tent"]:
            alive=False
        
        if coord[pos]["place"] and coord[pos]["arrow"]:
            aro+=1
        
        if coord[pos]["place"] and coord[pos]["seen"]==1 and coord[pos]["tent"]:
            num=list(coord.copy())
            pos=random.choice(num)
            coord[pos]["seen"]+=1
            coord[pos]["place"]=True
            moved=True
            
        elif coord[pos]["place"] and coord[pos]["tent"]:
            printer(coord, size)
            print("\n\nThe tentacles have pulled you under. You died!")
            
        elif coord[pos]["place"] and coord[pos]["mud"]:
            printer(coord,size)
            print("\n\nThe mud has collapsed. You died!")
        
        elif coord[pos]["place"] and coord[pos]["shrek"]:
            printer(coord,size)
            print("\n\nShrek has devoured your innards. You died!")
        
        
    
        
size=7
move(hazards(maker(size)),size)