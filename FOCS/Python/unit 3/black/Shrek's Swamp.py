import random


def maker(size,nested={}):
    for i in [(x, y) for y in range(size) for x in range(size)]:
        nested[i]={"seen": 0, "place": False,"tent": False, "mud": False, "shrek": False, "arrow": False, "tnear": False, "mnear": False, "snear": False}
    return nested


def hazards(coord, size, difficulty=1, test=False): # toggle test here
    num = list(coord.copy())

    shrek=random.choice(num)
    num.remove(shrek)
    coord[shrek]["shrek"], i=True, list(shrek)
    near=[(i[0],(i[1]+1)%size),((i[0]+1)%size,i[1]),((i[0]-1)%size,i[1]),(i[0],(i[1]-1)%size)]
    for cord in near:
        coord[cord]["snear"]=True

    aro=random.choice(num)
    num.remove(aro)
    coord[aro]["arrow"]=True

    pos=random.choice(num)
    num.remove(pos)
    coord[pos]["place"]=True
    coord[pos]["seen"]+=1

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
        near=[(i[0],(i[1]+1)%size),((i[0]+1)%size,i[1]),((i[0]-1)%size,i[1]),(i[0],(i[1]-1)%size)]
        for cord in near:
            coord[cord]["tnear"]=True

    for i in mud:
        coord[i]["mud"]=True
        i=list(i)
        near=[(i[0],(i[1]+1)%size),((i[0]+1)%size,i[1]),((i[0]-1)%size,i[1]),(i[0],(i[1]-1)%size)]
        for cord in near:
            coord[cord]["mnear"]=True

    if test:
        print("Tent:",tent)
        print("Mud:",mud)
        print("Shrek:",shrek)
        print("Arrow:",aro)
        print()

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


def updater(coord={}, pos=(), size=0, alive=True, win=False, aro=0, moved=False, leave=False,wrong=False, again=False):
    fill = "\n"+"-"*68

    if coord[pos]["snear"] or coord[pos]["tnear"] or coord[pos]["mnear"]:
        printer(coord, size)

        if coord[pos]["snear"]:
            print(fill+"\nYou catch a whiff of Shrek's foul odor..."+fill)

        if coord[pos]["tnear"]:
            print(fill+"\nYou feel something slimy clasp your leg..."+fill)

        if coord[pos]["mnear"]:
            print(fill+"\nYou feel the ground hardening beneath you..."+fill)

    if moved:
        print(fill+"\nThe tentacles have transported you to a different location!"+fill)
    elif leave:
        print(fill+"\nDid you really think you could escape Shrek's Swamp that easily?\n\nNo no, you shall not leave."+fill)
    elif wrong:
        print(fill+"\nThat is not a valid move.\n\nRemember: 'W' for up, 'A' for left, 'S' for down, and 'D' for right."+fill)
    elif aro==1:
        print(fill+"\nYou have acquired an arrow. Go shoot Shrek with it!"+fill)

    if win and aro==1:
        print(fill+"\nYour arrow flies true, right into Shrek's ear. You burn him from\ninside out and he dies! Now, you are free from the swamp!"+fill)
    elif not alive and aro==1:
        print(fill+"\nYou missed. Shrek finds you and rips off your ____!"+fill)

    if coord[pos]["place"] and coord[pos]["tent"]:
        printer(coord, size)
        print(fill+"\nThe tentacles have pulled you under. You died!"+fill)

    elif coord[pos]["place"] and coord[pos]["mud"]:
        printer(coord,size)
        print(fill+"\nThe mud has collapsed. You died!"+fill)

    elif coord[pos]["place"] and coord[pos]["shrek"]:
        printer(coord,size)
        print(fill+"\nShrek has devoured your innards. You died!"+fill)


def move(coord, size, alive=True, aro=0, moved=False, leave=False, wrong=False, win=False, again=False, inpu="yn"):
    fill = "\n"+"-"*68

    for i in coord:
        if coord[i]["place"]:
            pos=i

    while alive and not win and not again:

        print()
        printer(coord,size)
        print("\nYou are at position:",pos)
        updater(coord, pos, size, alive, win, aro, moved, leave, wrong)
        coord[pos]["place"], moved, leave, wrong = False, False, False, False

        inp=input("Where do you want to move? ").lower()

        tmp = list(pos)
        x,y = tmp[0], tmp[1]

        if aro==1:
            aro+=1

        if inp=="q":
            leave=True

        elif inp not in "swsasssd" or inp=="":
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


        elif inp == "sw" and aro>0:
            if coord[(x,(y-1)%size)]["shrek"]:
                win=True
            else:
                alive=False

        elif inp == "sa" and aro>0:
            if coord[((x-1)%size,y)]["shrek"]:
                win=True
            else:
                alive=False

        elif inp == "ss" and aro>0:
            if coord[(x,(y+1)%size)]["shrek"]:
                win=True
            else:
                alive=False

        elif inp == "sd" and aro>0:
            if coord[((x+1)%size,y)]["shrek"]:
                win=True
            else:
                alive=False

        if coord[pos]["mud"] or coord[pos]["shrek"]:
            alive=False

        elif coord[pos]["seen"]==2 and coord[pos]["tent"]:
            alive=False

        if coord[pos]["place"] and coord[pos]["arrow"]:
            aro+=1

        elif coord[pos]["place"] and coord[pos]["seen"]==1 and coord[pos]["tent"]:
            num=list(coord.copy())
            pos=random.choice(num)
            coord[pos]["seen"]+=1
            coord[pos]["place"], moved = True, True
        updater(coord, pos, size, alive, win, aro, moved, leave, wrong)

    while inpu in "yn" and win:
        inpu = input("\nDo you want to play again? ").lower()

        if inpu=="y":
            print("\n\nWelcome back, you fool")
            move(hazards(maker(size=7), size=7),size=7)

        elif inpu=="n":
            print("\n\nGood choice.")

    while inpu != "n" and not alive:
        inpu = input("\nDo you wish for more humiliation? ").lower()

        if inpu=="y":
            print(fill+"\nFool, why would you ever come back?"+fill)
            move(hazards(maker(size=7),size=7))

        elif inpu=="n":
            print("\nGood choice.")

        else:
            print(fill+"\nAnswer, or are you drowning in overwhelming terror?"+fill)


def reader(start, stop, strip):
    with open("dialogue.txt") as f:
        lines=f.readlines()
        if strip:
            for i in range(start, stop):
                print(lines[i].strip())
        else:
            for i in range(start, stop):
                print(lines[i])


def main(inp=""):
    s=("\n"+("-"*76))
    print(s+"\n\nWelcome to Shrek's Swamp!\n")
    reader(0,12,True)
    print(s)

    while inp != "q" and inp != "p":
        inp=input("Press 'C' for controls, 'B' for background, or 'P' to play! ").lower()

        while inp == "c":
            inpu=""
            inp=""
            print(s+"\n\n'W': move up\n'A': move left\n'S': move down\n'D': move right\n'S_': shoot in the chosen direction (ex. SW shoots up)\n'Q': exit (anywhere)\n"+s)
            while inpu != "q":
                inpu=input("Press 'Q' to go back: ").lower()
                print(s)

        while inp == "b":
            inpu=""
            inp=""
            x=0
            while inpu != "q" and x<6:
                if x==0:
                    print(s)
                    reader(12,14,False)
                    print(s)

                inpu=input("Press 'E' to continue or 'Q' to quit: ").lower()

                if inpu=="e":
                    x+=1


                if x==1:
                    print(s+"\n\n\nA sign nearby reads:\n\n ___________________________________________")
                    reader(19,36,True)
                    for i in range(9):
                        print("                    |   |")
                    print("                    |___|\n\n"+s)

                elif x==2:
                    print(s)
                    reader(48,50,False)
                    print(s)

                elif x==3:
                    print(s+"\n\n\nThe first one says:\n\n _________________________________________________")
                    reader(55,63,True)
                    for i in range(9):
                        print("                       |   |")
                    print("                       |___|\n\n"+s)

                elif x==4:
                    print(s+"\n\n\nThe second one says:\n\n _________________________________________________")
                    reader(79,87,True)
                    for i in range(9):
                        print("                       |   |")
                    print("                       |___|\n\n"+s)

                elif x==5:
                    print(s)
                    reader(99,108,True)
                    print(s)

                elif x==6:
                    print(s)
                    reader(108,110,False)
                    print(s)

        if inp=="p":
            print("\n\n     Welcome to Shrek's Swamp!")
            move(hazards(maker(size=7),size=7),size=7)

main()
