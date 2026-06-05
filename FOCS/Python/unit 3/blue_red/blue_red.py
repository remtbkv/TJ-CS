def printer(board):
    print("Current gameboard:" + "\n" + "-----------------------------")
    for i in board:
        print("| " + " | ".join(i) + " |")
    print("-----------------------------" + "\n" + "  0   1   2   3   4   5   6   ")

def determine(board):
    
    total="".join(["".join(i) for i in board])
    r_total=total[::-1]
    l=[]
    
    if str(board).count(".")==0:
        return 0
    
    for i in range(6):
        if "XXXX" in total[i*7:i*7+7]:
            return 1
        if "OOOO" in total[i*7:i*7+7]:
            return 2
    
    for col in range(7):
        if "XXXX" in total[col::7]:
            return 1
        elif "OOOO" in total[col::7]:
            return 2         
    
    for col in range(4):
        for i in range(3):
            ad=i*7
            l.append(total[3+ad+col:27+ad+col:6])
            l.append(total[ad+col:27+ad+col:8])
            
            l.append(r_total[ad+col:27+ad+col:8])
            l.append(r_total[6+ad-col:27+ad-col:6])
    if "XXXX" in l:
        return 1
    elif "OOOO" in l:
        return 2

def turn(board):
    if str(board).count("X")==str(board).count("O"):
        print("\n" + "Player X's turn.")
    elif str(board).count("X")>str(board).count("O"):
        print("\n" + "Player O's turn.")

def move_maker(board,type):
    printer(board)
    turn(board)

    col_counter=[0, 0, 0, 0, 0, 0, 0]
        
    if type=="l":
        for row in range(6):
            for column in range(7):
                if board[-(row+1)][column] != ".":
                    col_counter[column]+=1
    
    col = ""

    while col != "s" and col != "q" and determine(board)!=0 and determine(board)!=1 and determine(board)!=2:
        col = input("Choose your column (0-6), (S) to save and quit, or (Q) to quit: ").lower()
        
        if not col.isdigit() and col != "s" and col != "q":
            print("\n" + "You silly goose. What do you think you're doing?")
        
        elif col.isdigit():
            if -1<int(col)<7 and col_counter[int(col)]<6:
                
                if str(board).count("X")==str(board).count("O"):
                    board[5-(col_counter[int(col)])][int(col)]="X"
                    col_counter[int(col)] += 1
                else:
                    board[5-(col_counter[int(col)])][int(col)]="O"
                    col_counter[int(col)] += 1  
        
                print()
                printer(board)
                turn(board)
                
                if determine(board)==0:
                    print("\n"+"Nobody won!  (HAHAHA imagine actually tying in a simple game of connect 4)")
                elif determine(board)==1:
                    print("\n"+"Winner is Player 1: 'X'!  (Dont worry first player is always rigged to win)")
                elif determine(board)==2:
                    print("\n"+"Winner is Player 2: 'O'!  (HAHAHA imagine going first and still losing)")
            else:
                print("\n"+"You silly clown. What are you doing all the way up there?")
        if col=="s":
            lst=["".join(i) for i in board]
            with open("savegame.txt", "w") as g:
                for i in lst:
                    g.write("".join(i)+"\n")
            print("\n" + "Successfully saved and closed the game")
        elif col=="q":
            print("\n" + "Successfully closed the game")

def main(board=[]):
    choice=input("Choose to load new game (N) or load from a saved file (L): ").lower()
    
    while choice != "n" and choice != "l":
        choice = input("Input the right thing, you fool: (N) or (L): ")
    
    if choice=="n":
        board=[['.', '.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.', '.']]
        
    else:
        with open("savegame.txt") as f:
            for i in f:
                board.append(list(i.strip()))
    print()
    move_maker(board,str(choice))


main()