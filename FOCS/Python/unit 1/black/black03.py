def swap(l,x):
    temp=l[x]
    l[x]=l[x+1]
    l[x+1]=temp
    return l

def sort_string(s,x=0,y=0):
    l=list(s)

    if x==len(s)-1 and y!=0:
        return sort_string("".join(l))

    elif x==len(s)-1 and y==0:
        return "".join(l)

    elif l[x]>l[x+1]:
        return sort_string("".join(swap(l,x)),x+1,y+1)

    elif l[x]<l[x+1] or l[x]==l[x+1]:
        return sort_string("".join(l), x+1,y)


def reverse_sort_string(s,x=0,y=0):
    l=list(s)

    if x==len(s)-1 and y!=0:
        return reverse_sort_string("".join(l))

    elif x==len(s)-1 and y==0:
        return "".join(l)

    elif l[x]<l[x+1]:
        return reverse_sort_string("".join(swap(l,x)),x+1,y+1)

    elif l[x]>l[x+1] or l[x]==l[x+1]:
        return reverse_sort_string("".join(l), x+1,y)


def vowels_first(s,v="",x=0):
    l=list(s)

    if x==len(s)-1:
        return sort_string(v) + sort_string(s)

    elif l[x] in "aeiou":
        v+=l[x]
        del l[x]
        return vowels_first("".join(l),v,x)
    else:
        return vowels_first(s,v,x+1)

import sys
print(sort_string(sys.argv[1]))
print(reverse_sort_string(sys.argv[1]))
print(vowels_first(sys.argv[1]))
