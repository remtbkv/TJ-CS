alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

import math
def mod_inverse_helper(a, b):
    q, r = a//b, a%b
    if r == 1:
        return (1, -1 * q)
    u, v = mod_inverse_helper(b, r)
    return (v, -1 * q * v + u)
def mod_inverse(a, m):
    assert math.gcd(a, m) == 1, "You're trying to invert " + str(a) + " in mod " + str(m) + " and that doesn't work!"
    return mod_inverse_helper(m, a)[1] % m

def affine_encode(message, a, b):
    l=[]
    for letter in message:
        i=alpha.index(letter)
        compute=(a*i+b)%26
        l.append(alpha[compute])
    return "".join(l)

def affine_decode(encoded, a, b):
    l=[]
    for letter in encoded:
        i=alpha.index(letter)
        compute=(mod_inverse(a,26)*(i-b))
        l.append(alpha[compute%26])
    return "".join(l)

def convert_to_num(ngraph):
    power=0
    sum=0
    for i in ngraph:
        sum+=alpha.index(i)*(26**power)
        power+=1
    return sum

def convert_to_text(num, n):
    if n==1:
        return alpha[num%26]
    else:
        return alpha[num%26]+(convert_to_text(num//26,n-1))

def affine_n_encode(text, n, a, b):
    ngraphs=[]
    converted=[]
    for i in range(0,len(text),n):
        if i+n>len(text):
            ngraphs.append(text[i]+"X"*(n-len(text)%n))
        else:
            ngraphs.append(text[i:i+n])
    for i in ngraphs:
        c=convert_to_num(i)
        apply=(a*c+b)%26**n
        converted.append(convert_to_text(apply,len(i)))
    return "".join(converted)

def affine_n_decode(text, n, a, b):
    ngraphs=(text[i:i+n] for i in range(0,len(text),n))
    converted=[]
    for i in ngraphs:
        c=convert_to_num(i)
        compute=mod_inverse(a,26**n)*(c-b)
        converted.append(convert_to_text(compute,len(i)))
    return "".join(converted)

import sys
text, dec1, dec2 = sys.argv[1:4]
a, b, n, n_a, n_b = [int(x) for x in sys.argv[4:]]
print(affine_encode(text, a, b))
print(affine_decode(dec1, a, b))
print(affine_n_encode(text, n, n_a, n_b))
print(affine_n_decode(dec2, n, n_a, n_b))