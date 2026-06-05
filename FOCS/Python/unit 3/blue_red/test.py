board=[]

# with open("savegame.txt") as f:
#     for i in f:
#         board.append(list(i.strip()))

board=[['1', '2', '3', '4', '5', '6', '7'], ['2', '3', '4', 'z', '6', '7', '8'], ['3', '4', 'y', 'd', '7', '8', '9'], ['4', 'x', 'c', '7', '8', '9', '0'], ['w', 'b', '7', '8', '9', '0', '1'], ['a', '7', '8', '9', '0', '1', '2']]
total="".join(["".join(i) for i in board])
r_total=total[::-1]

for i in board:
    print("| " + " | ".join(i) + " |")
print("-----------------------------" + "\n" + "  0   1   2   3   4   5   6   ")
print()
print("Total:",total)
print("Reverse:",r_total)
print()

# for col in range(4): # bottom right
#     for i in range(3):
#         ad=i*7
#         print(r_total[ad+col:27+ad+col:8])
#     print("DONE"+"\n")

print(r_total[0+1:27+1:8])

# l=[]
# for col in range(4):
#     for i in range(3):
#         ad=i*7
#         l.append(total[3+ad+col:27+ad+col:6]), l.append(total[ad+col:27+ad+col:8]), l.append(r_total[ad+col:27+ad+col:8]), l.append(r_total[6+ad-col:27+ad-col:6])

# if "XXXX" in l:
#     print(1)
# elif "OOOO" in l:
#     print(2)

'''


for col in range(4): # top left
    for i in range(3):
        ad=i*7
        print(total[ad+col:27+ad+col:8])

for col in range(4): # bottom right
    for i in range(3):
        ad=i*7
        print(r_total[ad+col:27+ad+col:8])
        
'''

# for col in range(4): # bottom left
#     for i in range(3):
#         ad=i*7
#         print(r_total[6+ad-col:27+ad-col:6])




# def move_maker(board,type):
#     printer(board)
#     turn(board)

#     col_counter=[0, 0, 0, 0, 0, 0, 0]
        
#     if type=="l":
#         for row in range(6):
#             for column in range(7):
#                 if board[-(row+1)][column] != ".":
#                     col_counter[column]+=1
    
#     cho="Choose your column (0-6) or (S) to save and quit, or (Q) to quit: "
#     col = input(cho).lower()
    
#     while col != "s" and col != "q" and not col.isdigit():
#         print("\n"+"Try again buddy. Do you not know how to read?")
#         col = input(cho).lower()
    
#     while col.isdigit():
#         c=int(col)
        
#         while col != "s" and col != "q" and not col.isdigit():
#             print("\n"+"Try again buddy. Do you not know how to read?")
#             col = input(cho).lower()
        
#         while c>6:
#             print("\n"+"Try again buddy. Do you not know how to count?")
#             col = input(cho).lower()
        
#         if col_counter[c]==6:
#             print("\n"+"Try again buddy. Do you not see this column is full?")
#             col = input(cho).lower()
        
#         if col_counter[c]<6 and -1<c<7:
            
#             if str(board).count("X")==str(board).count("O"):
#                 board[5-(col_counter[c])][c]="X"
#                 col_counter[c] += 1
#             else:
#                 board[5-(col_counter[c])][c]="O"
#                 col_counter[c] += 1
            
#             print()
#             printer(board)
#             turn(board)
             
#             if determine(board)==0:
#                 print("\n"+"Nobody won!  (HAHAHA imagine actually tying a simple game of connect 4)")
#                 break
#             elif determine(board)==1:
#                 print("\n"+"Winner is Player 1: 'X'!  (Dont worry first player is always rigged to win)")
#                 break
#             elif determine(board)==2:
#                 print("\n"+"Winner is Player 2: 'O'!  (HAHAHA imagine going first and still losing)")
#                 break
            
#             col = input(cho).lower()
#             c=int(col)
            
#             if col_counter[c]==6:
#                 while c==6:
#                     print("\n"+"Try again buddy. Do you not see this column is full?")
#                     col = input(cho).lower()
    
#             elif col != "s" and col != "q" and not col.isdigit():
#                 while col != "s" and col != "q" and not col.isdigit():
#                     print("\n"+"Try again buddy. Do you not know how to read?")
#                     col = input(cho).lower()
    
#         if col != "s" and col != "q" and not col.isdigit():
#             print("\n"+"Try again buddy. Do you not know how to read?")
#             col = input(cho).lower()
        
#         elif c>6:
#             print("\n"+"Try again buddy. Do you not know how to count?")
#             col = input(cho).lower()
        
