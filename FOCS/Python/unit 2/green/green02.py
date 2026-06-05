alpha="ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def caesar_encode(text, shift):
    l=[]
    for i in text:
        index=alpha.index(i)
        l.append(alpha[(index+shift)%26])
    return "".join(l)

def caesar_decode(text, shift):
    l=[]
    for i in text:
        index=alpha.index(i)
        l.append(alpha[(index-shift)%26])
    return "".join(l)

def caesar_crack(text):
    for i in range(26):
        print(caesar_decode(text,i))

def substitution_encode(text, code_alpha):
    l=[]
    for i in text:
        index=alpha.index(i)
        l.append(code_alpha[index%26])
    return "".join(l)

def substitution_decode(text, code_alpha):
    l=[]
    for i in text:
        index=code_alpha.index(i)
        l.append(alpha[index%26])
    return "".join(l)

import sys
pt = sys.argv[1]
a2 = sys.argv[2]
ct = sys.argv[3]
ct2 = sys.argv[4]
shift = int(sys.argv[5])
print(caesar_encode(pt, shift))
print(caesar_decode(ct, shift))
print(substitution_encode(pt, a2))
print(substitution_decode(ct2, a2))
print(caesar_crack(ct))