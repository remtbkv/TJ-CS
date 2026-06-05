import sys
sys.setrecursionlimit(99999)

alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def c_sub(text):
    choice = ""
    while choice != "quit":
        l=[]
        print("Your text: ", text)
        print("")
        for i in alpha:
            l.append((i + ": " + str(text.count(i))))
        print("|"," | ".join(l[:13]), "|")
        print("|"," | ".join(l[13:]), "|")
        print("")      
        print("Reminder: most common letters are E, T, A, O, I, N, S, H, R, D, L, U")
        choice=input("Type a pair of letters to swap, for example AB would swap A and B, or type 'quit': ")
        lst_ch=list(choice)
        text=text.replace(lst_ch[0],"0")
        text=text.replace(lst_ch[1],lst_ch[0])
        text=text.replace("0",lst_ch[1])

c_sub(sys.argv[1])