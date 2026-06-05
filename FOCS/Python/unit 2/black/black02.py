def simple_columnar_encode(text, c, fill):
    fill_txt = text+("X"*(c-(len(text)%c)))    
    l=""
    if fill:
        for i in range(c):
            l+=fill_txt[i::c]
    else:
        for i in range(c):
            l+=text[i::c]
    return l

def simple_columnar_decode(text, c):
    n=len(text)//c
    n_rows=-(-n)//1
    l=""

    if len(text)%c==0:
        for i in range(n_rows):
            l+=text[i::n_rows]
    
    else:
        max_rows= -(-len(text)//c)//1
        prob_rows= len(text)//c
        extra= len(text)%c
        ll=""

        lst=[]
        lst2=[]

        for i in range(0,(max_rows*extra),max_rows):
            lst.append(text[i:i+max_rows])
        for i in range((max_rows)*extra,len(text),prob_rows):
            lst.append(text[i:i+prob_rows])
        for part in lst:
            lst2.append(list(part))

        for i in range(c):
            for counter in range(prob_rows):
                ll+=(lst2[i][counter])

        for i in range(prob_rows):
            l+=ll[i::prob_rows]

        extra2=len(text)%c

        for i in range(extra2):
            l+=lst2[i][-1]
    return l

def keyword_columnar_encode(text, keywd, fill):
    dict={}
    l=[]
    c=len(keywd)
    output=""
    fill_txt=text+("X"*(c-(len(text)%c)))

    for index, letter in enumerate(sorted(keywd)):
            dict[letter]=index

    if fill==True:
        for i in dict:
            ind=keywd.index(i)
            l.append(text[ind])

        for i in l:
            output+=text[text.index(i)::c]

    else:
        for i in dict:
            ind=keywd.index(i)
            l.append(fill_txt[ind])

        for i in l:
            output+=fill_txt[fill_txt.index(i)::c]

    return output

def col_reader_spreader(text, keywd):
    lst=[]
    prob_rows=len(text)//len(keywd)
    for i in range(prob_rows):
        lst.append(text[i::prob_rows])
    return lst

def key_full_decode(text, keywd, dict2):
    output=""
    for i in col_reader_spreader(text, keywd):
        for index,letter in enumerate(i):
            output+=i[dict2.get(index)]
    return output

def keyword_columnar_decode(text, keywd):

    dict={}
    dict2={}
    l=[]

    # sorts each letter in alphabetical order:
    for index, letter in enumerate(sorted(keywd)):
        dict[letter]=index

    for i in keywd:
        l.append(dict.get(i))

    # assigns each alphabetized value to their consecutive indices starting from 0 (to dict2):
    for index, value in enumerate(l):
        dict2[index]=value
    
    if len(text)/len(keywd)==int(len(text)/len(keywd)):
        return key_full_decode(text, keywd, dict2)

    else:
        c=len(keywd)
        prob_rows= len(text)//c
        extra= len(text)%c

        l=[]
        for i in range(c):
            while extra>0:
                l.append(1)
                extra-=1
            l.append(0)

        sorted_l=[]
        for i in range(c):
            sorted_l.append(l[keywd.index(sorted(keywd)[i])])
        l_text=list(text)
        counter=0
        for i in range(prob_rows,len(l_text),prob_rows):
            if sorted_l[counter]==0:
                l_text.insert(i+counter,"-")
            counter+=1
        
        almost= list(key_full_decode("".join(l_text), keywd, dict2))
        for i in almost:
            while almost.count("-")>0:
                almost.remove("-")
        return "".join(almost)


from nltk.corpus import words
from itertools import permutations

def bruteforcer(s, min_prob_length=2, max_prob_length=6, expected=5, put={}, l=[i for i in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"], w=[w for w in words.words() if len(w)>2]):
    for x in range(min_prob_length, max_prob_length+1):
        for i in permutations(l[:x]):
            d = keyword_columnar_decode(s, "".join(i)).lower()
            if len([word for word in w if word in d])>9:
                put[d]=i
        print(len(l[:x]))
        print(put,sep="\n")
        print("\n\n\n")

# bruteforcer("", min_prob_length=4, max_prob_length=8)


import sys
a = sys.argv[1]
b = int(sys.argv[2])
c = sys.argv[3]
d = sys.argv[4]
e = sys.argv[5]
print(simple_columnar_encode(a, b, True))
print(simple_columnar_encode(a, b, False))
print(simple_columnar_decode(d, b))
print(keyword_columnar_encode(a, c, True))
print(keyword_columnar_encode(a, c, False))
print(keyword_columnar_decode(e, c))