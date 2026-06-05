def slice_end(s, i):
    print(s[i:])

def pig_latin(string):
    s = string
    x = s[1:len(s)]
    y = "ay"
    print(x+y)

def shrink(s):
    if len(s)==0:
        return
    print(s)
    shrink(s[0:len(s)-1])

def grow(s):
    if len(s)==0:
        return
    grow(s[:len(s)-1])
    print(s)

def shrink_right(s, x=0):
    if len(s)==0:
        return 
    print(" "*x+s)
    shrink_right(s[1:], x+1)

def word_cascade(s):
    grow(s[:len(s)-1]) 
    shrink_right(s)

def grow_left(s, x=0):
    if len(s)==0:
        return
    grow_left(s[1:], x+1)
    print(" " *x+s)

def cascade_backwards(s):
    grow_left(s)
    shrink(s[:len(s)-1])

def snake(s, x=0):
    l=[0, 1, 2, 1]
    if x==len(s):
        return
    print(" "*l[x%4]+s[x])
    snake(s, x+1)

def custom_snake(s, n, x=0):
    l1=list(range(0,n))
    l2=list(range(1, n-1))
    l2.sort(reverse=True)
    l3=l1+l2
    if x==len(s):
        return
    print(" "*(l3[x%(len(l3))])+s[x])
    custom_snake(s, n, x+1)

'''
def lst(n):
    l1=list(range(0,n))
    l2=list(range(1, n-1))
    l2.sort(reverse=True)
    l3=l1+l2
    return l3

def custom_snake(s, n, x=0):
    y=(len(lst(n)))
    if x==len(s):
        return
    print(" "*(lst(n)[x%y])+s[x])
    custom_snake(s, n, x+1)
'''

import sys
s = sys.argv[1]
print("Shrink:")
print()
shrink(s)
print()
print("Grow:")
print()
grow(s)
print()
print("Shrink right:")
print()
shrink_right(s)
print()
print("Word cascade:")
print()
word_cascade(s)
print()
print("Cascade backwards:")
print()
cascade_backwards(s)
print()
print("Snake:")
print()
snake(s)
print()
print("Custom snake:")
print()
custom_snake(s, int(sys.argv[2]))