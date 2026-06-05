def pyramid(s, x=0):
    l=len(s)
    if l==0:
        return
    pyramid(s[1:l-1], x+1)
    print(" "*x+s)

def spike(s, x=0):
    l=len(s)
    if x==l:
        return
    print(" " * x + s[x:])
    spike(s[0:l-1], x+1)

def diamond(s,x=1):
    l=len(s)
    if x==1:
        pyramid(s)
    elif x==l:
        return
    print(" " * x + s[x:l-1])
    diamond(s[0:l-1], x+1)

def sidewinder(s, x=0):
    if x==0:
        print("   ".join(s[0::4]))
        sidewinder(s,x+1)
    if x==1:
        print(" "+" ".join(s[1::2]))
        sidewinder(s,x+1)
    if x==2:
        print("  "+"   ".join(s[2::4]))

def separator(s,l=[],x=0):
    if x==len(s):
        return l
    elif x==0:
        l=[]
        l.append(s[x])
        return separator(s,l,x+1)
    elif x>0:
        l.append(s[x])
        return separator(s,l,x+1)

def combiner(l1, l2, x=0, y=1):
    if x==len(l2):
        return l1
    else:
        l1.insert(y, l2[x])
        return combiner(l1, l2, x+1, y+2)

def inserter(n, l, b_space, x, z=0, y=0):
    if z==len(l):
        return "".join(l)
    elif z==0:
        l.insert(0, x*" ")
        return inserter(n, l, b_space, x, z+2, y) 
    elif y%2==0:
        l.insert(z, b_space*" ")
        return inserter(n, l, b_space, x, z+2, y+1)
    elif y%2==1:
        l.insert(z, ((x+(x-1))*" "))
        return inserter(n, l, b_space, x, z+2, y+1)        

def custom_sidewinder(s, n, x=0):
    magic=(n-2)*2
    omagic=(n-1)*2

    if x==0:
        print(((magic+1)*" ").join(separator(s[::omagic])))
        custom_sidewinder(s, n, x+1)
    elif 0<x<n-1:
        print(inserter(n, combiner(separator(s[x::omagic]), separator(s[omagic-x::omagic])), magic+1-(2*x), x))
        custom_sidewinder(s, n, x+1)
    elif x==n-1:
        print((n-1)*" " + ((magic+1)*" ").join(separator(s[n-1::omagic])))

def top(s, n):
    print(s[:n//2+1]+"   "+s[n//2:])
    print(s[:n//2]+"     "+s[n//2+1:])
    
def bot(s, n):
    print(s[:n//2]+"     "+s[n//2+1:])
    print(s[:n//2+1]+"   "+s[n//2:])

def mid(s, n):
    print("   "+s[1:-1])
    print("  "+s)
    print("   "+s[1:-1])

def m_top(s, n, x=0):
    m=n//2
    if x==m-2:
        print(s[:m-1-x]+"   "+ s[m-x:m+1+x] + "   " + s[-(m-1-x):])
    else:
        print(s[:m-1-x]+"   "+ s[m-x:m+1+x] + "   " + s[-(m-1-x):])
        m_top(s, n, x+1)

def m_bot(s, n, x=0):
    m=n//2
    if x==m-2:
        print(s[:x+1]+"   "+ s[m-(m-1)+x:m-(n-(m-2))-x] + "   " + s[-(x+1):])
    else:
        print(s[:x+1]+"   "+ s[m-(m-1)+x:m-(n-(m-2))-x] + "   " + s[-(x+1):])
        m_bot(s, n, x+1)

def magic_square(s, x=0):
    n=len(s)
    if n==3:
        top(s, n)
        mid(s, n)
        bot(s, n)
    elif x==0:
        top(s, n)
        magic_square(s, x+1)
    elif x==1:
        m_top(s, n)
        magic_square(s, x+1)
    elif x==2:
        mid(s, n)
        magic_square(s, x+1)
    elif x==3:
        m_bot(s, n)
        magic_square(s, x+1)
    elif x==4:
        bot(s, n)

def word_art_19(s, x=0,y=0): # Hourglass, only odd length strings
    n=len(s)
    if x==0:
        print(s)
        word_art_19(s,x+1)
    elif x < n//2:
        print(" "*x + s[x] + " "*((n-2-(2*x))) + s[-(x+1)])
        word_art_19(s, x+1)
    elif x == n//2:
        print(" "*x+s[x])
        word_art_19(s,x+1)
    elif x == n//2+1 and y < n//2-1:
        print(" "*(n//2-y-1) + s[n//2-1-y] + " "*(y*2+1) + s[n//2+1+y])
        word_art_19(s,x,y+1)
    elif y==n//2-1:
        print(s)

import sys
s = sys.argv[1]
print("Pyramid:")
print()
pyramid(s)
print()
print("Spike:")
print()
spike(s)
print()
print("Diamond:")
print()
diamond(s)
print()
print("Magic square:")
print()
magic_square(s)
print()
print("Sidewinder:")
print()
sidewinder(s)
print()
print("Custom sidewinder:")
print()
custom_sidewinder(s, int(sys.argv[2]))
print()
print("Hourglass:")
print()
word_art_19(s)
print()