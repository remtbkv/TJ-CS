alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def stringify(message, key):
    l=[]
    for i in range(len(message)):
        l.append(key[(i%(len(key)))])
    return "".join(l)

def vigenere_encode(message, key):
    l=[]
    keyword=stringify(message,key)
    counter=0
    for counter in range(len(message)):
        m=message[counter]
        k=keyword[counter]
        added=(alpha.index(m)+alpha.index(k))%26
        l.append(alpha[added])
        counter+=1
    return "".join(l)

def vigenere_decode(message, key):
    l=[]
    keyword=stringify(message,key)
    counter=0
    for counter in range(len(message)):
        m=message[counter]
        k=keyword[counter]
        added=(alpha.index(m)-alpha.index(k))%26
        l.append(alpha[added])
        counter+=1
    return "".join(l)

import sys
pt = sys.argv[1]
ct = sys.argv[2]
ky = sys.argv[3]
print(vigenere_encode(pt, ky))
print(vigenere_decode(ct, ky))