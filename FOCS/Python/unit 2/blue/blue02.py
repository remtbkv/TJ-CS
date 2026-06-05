import sys
sys.setrecursionlimit(999999)

alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

eng_freq = [.0817, .0149, .0278, .0425, .1270, .0223, .0202, .0609, .0697, .0015, .0077, .0403, .0241, .0675, .0751,
            .0193, .0010, .0599, .0633, .0906, .0276, .0098, .0236, .0015, .0197, .0007]

eng_freq_squared = []
for freq in eng_freq:
    eng_freq_squared.append(freq * freq)
engIoC = sum(eng_freq_squared)


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

def i_of_c(text):
    n=len(text)
    lst=[]
    lst2=[]
    for i in alpha:
        lst.append(text.count(i))
    for i in lst:
        lst2.append((i/n)*((i-1)/(n-1)))
    return sum(lst2)

def friedman_test(text):
    c=1/26
    n=len(text)
    i=i_of_c(text)
    e=engIoC
    return (n*(e-c))/((i*(n-1))+e-(n*c))

def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)
def gcd_n(lst, counter=0):
    if counter==(len(lst)-1):
        return lst[counter]
    else:
        return gcd(lst[counter], gcd_n(lst, counter+1))
def find_plausible_gcd(distances,minimum=1):
    l=[]
    for i in distances:
        if distances.count(i)>minimum:
            l.append(i)
    if gcd_n(l)>1:
        return gcd_n(l)
    else:
        find_plausible_gcd(distances,minimum+1) 

def kasiski_test(text):
    trigraphs=[text[i:i+3] for i in range(len(text)-2)]
    distances=[]
    for i in range(len(text)-2):
        trigraph=text[i:i+3]
        if trigraph in trigraphs:
            distances.append(i-trigraphs.index(trigraph))            
    return find_plausible_gcd(distances)

def make_cosets(text,x):
    l=[]
    for i in range(x):
        l.append(text[i::x])
    return l

def find_total_difference(l1, l2):
    l=[]
    for i in range(26):
        l.append(abs(l1[i]-l2[i]))
    return sum(l)

def find_likely_letter(coset):
    freq_list=[]
    lst_rot=[]
    for i in alpha:
        freq_list.append(coset.count(i)/len(coset))
    for i in range(26):
        freq_list.append(freq_list[0])
        del freq_list[0]
        compare=find_total_difference(freq_list,eng_freq)
        lst_rot.append(compare)
    return alpha[(lst_rot.index(min(lst_rot))+1)%26] # output is 1 letter off for each letter

def crack(text):
    print("Your encrypted text is: ", text)
    print("")
    print("Friedman Test gives estimated key length of: ", friedman_test(text))
    print("Kasiski Test gives estimated key length of: ", kasiski_test(text))
    print("")
    x=input("Choose the key length you want to try: ", )
    cosets=make_cosets(text, int(x))
    for i in cosets:
        print("For coset ", cosets.index(i), ", the most likely letter is: ", find_likely_letter(i))
    c=input("Type the key you would like to decipher with: ", )
    print("")
    print("Your decoded text is:",vigenere_decode(text,c))


import sys
crack(sys.argv[1])