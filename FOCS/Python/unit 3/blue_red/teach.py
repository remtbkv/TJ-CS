board=[['.', '.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.', '.']]

def printer(board):
    print("Current gameboard:" + "\n" + "-----------------------------")
    for i in board:
        print("| " + " | ".join(i) + " |")
    print("-----------------------------" + "\n" + "  0   1   2   3   4   5   6   ")



def move(board):
    
    printer(board)
    
    col_counter=[0, 0, 0, 0, 0, 0, 0]
    
    col = ""
    
    while col != "Q":
        col= input("choose your column: ")
        1
        if col.isdigit():
            c=int(col)
            
            if -1 < c < 7 and col_counter[c] < 6:
                
                if str(board).count("X")==str(board).count("O"):
                    board[5-(col_counter[c])][c]="X"
                    col_counter[c] += 1
                
                elif str(board).count("X")>str(board).count("O"):
                    
                    board[5-(col_counter[c])][c]="O"
                    col_counter[c] += 1
                printer(board)
                

move(board)