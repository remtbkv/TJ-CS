import random

def hazards(coord): 
    num = list(coord.copy())
    shrek=random.choice(num) # 43
    num.remove(shrek)
    
    tent = [] # 13, 8
    tent1=random.choice(num)
    tent.append(tent1), num.remove(tent1)
    tent2=random.choice(num)
    tent.append(tent2), num.remove(tent2)
    
    mud = random.choice(num) # 22


def printer(coord,x=0):
    lst=list(coord.values())
    print("     0   1   2   3   4   5   6" + "\n"+"   -----------------------------")
    for i in range(7,43,7):
        print(x," | " + " | ".join(lst[i-7:i]) + " |" +"\n")
        x+=1
    print(x, " | " + " | ".join(lst[42:49]) + " |")
    print("   -----------------------------")


def o_printer(coord):
    coord=list(coord)
    coordo=[]
    for i in coord:
        coordo.append(str(i))
    print(" " + "\n" + "----------------------------------------------------------------")
    for i in range(7,43,7):
        print("| " + " | ".join(coordo[i-7:i]) + " |" +"\n")
    print("| " + " | ".join(coordo[42:49]) + " |")
    print("----------------------------------------------------------------")



def move(coord):
    num=list(coord.copy())
    pos=random.choice(num)
    coord.update({pos: "O"})
    arrows=2
    
    printer(coord)
    print("\n" + "You are at position:",pos)    
    print("Arrows:",arrows)
    
    alive=True
    fill="-"*64
    
    while alive:
        inp=input("Where do you want to move? ").lower()
        
        tmp = list(pos)
        x=int(tmp[0])
        y=int(tmp[1])
        
        if inp not in "wasdq":
            print("\n"+fill+"----\nThat is not a valid move.\n\nRemember: 'W' for up, 'A' for left, 'S' for down, and 'D' for right.\n"+fill+"----")
        
        elif inp=="q":
            print("\n"+fill+"\nDid you really think you could escape Shrek's Swamp that easily?\n\nNo no, you shall not leave.\n"+fill)
            
        elif inp == "w":
            pos=(x,(y-1)%7)
            
            print(pos)
            
        elif inp == "a":
            pos=((x-1)%7,y)
            
            print(pos)
            
        elif inp == "s":
            pos=(x,(y+1)%7)
            
            print(pos)
            
        elif inp == "d":
            pos=((x+1)%7,y)
            
            print(pos)
            
def reader(start, stop, strip):
    with open("dialogue.txt") as f:
        lines=f.readlines()
        if strip:
            for i in range(start, stop):
                print(lines[i].strip())
        else:
            for i in range(start, stop):
                print(lines[i])


def main(coord= {(0, 0): " ", (1, 0): " ", (2, 0): " ", (3, 0): " ", (4, 0): " ", (5, 0): " ", (6, 0): " ", (0, 1): " ", (1, 1): " ", (2, 1): " ", (3, 1): " ", (4, 1): " ", (5, 1): " ", (6, 1): " ", (0, 2): " ", (1, 2): " ", (2, 2): " ", (3, 2): " ", (4, 2): " ", (5, 2): " ", (6, 2): " ", (0, 3): " ", (1, 3): " ", (2, 3): " ", (3, 3): " ", (4, 3): " ", (5, 3): " ", (6, 3): " ", (0, 4): " ", (1, 4): " ", (2, 4): " ", (3, 4): " ", (4, 4): " ", (5, 4): " ", (6, 4): " ", (0, 5): " ", (1, 5): " ", (2, 5): " ", (3, 5): " ", (4, 5): " ", (5, 5): " ", (6, 5): " ", (0, 6): " ", (1, 6): " ", (2, 6): " ", (3, 6): " ", (4, 6): " ", (5, 6): " ", (6, 6): " "}):
    print("Welcome to Shrek's Swamp!\n")
    
    reader(0,12,True)
            
    inp=""
    
    while inp != "q" and inp != "p":
        inp=input("Press 'C' for controls, 'B' for background, or 'P' to play! ").lower()
        
        while inp == "c":
            inpu=""
            inp=""
            print("\n'W': move up\n'A': move left\n'S': move down\n'D': move right\n'S_': shoot in the chosen direction (ex. SW shoots up)\n'Q': exit (anywhere)")
            while inpu != "q":
                inpu=input("Press 'Q' to go back: ").lower()
        
        while inp == "b":
            inpu=""
            inp=""
            x=0
            while inpu != "q" and x<6:
                if x==0:
                    reader(12,14,False)
                
                inpu=input("Press 'E' to continue or 'Q' to quit: ").lower()
                
                if inpu=="e":
                    x+=1
                
                    
                if x==1:
                    print("\n\nA sign nearby reads:\n\n ___________________________________________")
                    reader(19,36,True)
                    for i in range(9):
                        print("                    |   |")
                    print("                    |___|\n")
                
                elif x==2:
                    reader(48,50,False)
                
                elif x==3:
                    print("\n\nThe first one says:\n\n _________________________________________________")
                    reader(55,62,True)
                    for i in range(9):
                        print("                       |   |")
                    print("					   |___|\n")
                
                elif x==4:
                    print("\n\nThe second one says:\n\n _________________________________________________")
                    reader(78,86,True)
                    for i in range(9):
                        print("                       |   |")
                    print("					   |___|\n")
                
                elif x==5:
                    reader(98,106,True)
                    
                elif x==6:
                    reader(106,108,False)

                
        if inp=="p":
            print("\n\n")
            move(coord)
            
      

main()


'''
assign boolean values to whether u have seen the square, it has a hazard, or more


. - safe
~ - tentacles
D - dry mud
* - shrek




randint(a, b)
randrange(10) 
choice(['win', 'lose', 'draw']) 

deck = 'ace two three four'.split()
shuffle(deck)                       # Shuffle a list
deck

'''