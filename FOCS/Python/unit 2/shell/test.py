'''
ZIASEKTBEGRTRAOALES

ZIASEK
TBEGRT
RAOALE
S

Z R I T A R S
E A K O T A
B L E E G S

ZEBRALIKETOEATGRASS

ZEBRAL
IKETOE
ATGRAS
S

ZIASEK
TBEGRT
RAOALE
S
'''


'''
text="ZIASEKTBEGRTRAOALES"
c=6
n=len(text)//c

lst2= ['ZRITARS', 'EAKOTA', 'BLEEGS']
# txt="ZRITARSEAKOTABLEEGS" # len = 19
txt = [] #figure this out
lst=[]
for part in lst2:
   lst.append(list(part))

l=[]
max_rows_new=len(txt)//c
extra=len(txt)%c

for i in range(c):
    for counter in range(max_rows_new):
        l.append(lst[counter][i])
for i in range(extra):
    l.append(lst[i][c+i])
print("".join(l))



def len_lst(text,c):
    l1=[]
    for i in range(0,len(text),c):
        l1.append(text[i:i+c])
    return len(l1[1])

def len_lst_3(text,c):
    l1=[]
    for i in range(0,len(text),c):
        l1.append(text[i:i+c])
    return len(l1[2])

def simple_columnar_decode(text, c):
    n_rows=-(-len(text)//c)//1
    ll=2*len_lst(text,c)
    lll=3*len_lst_3(text,c)
    l=""
    if len(text)%c==0:
        for i in range(n_rows):
            l+=text[i::n_rows]
    elif n_rows==2:
        l+=(text[:ll][::2]) + (text[ll:]) + (text[:ll][1::2])
    elif n_rows==3:
        l+=(text[:lll][::3]) + (text[lll:-1][::2]) + (text[:lll][1::3]) + (text[lll:][1::2]) + (text[:lll][2::3])
            #AT                     #TAC                   #KA                  #TDA                     #AWN
    return l

'''

def make_raw_s(text,c):
    l=[]
    for i in range(0,len(text),c):
        l.append(text[i:i+c])
    return "\n".join(i for i in l)
    #return l

# print(make_raw_s(text,5))

encoded="HDEXYATXESSXTNHXUYLXSEKXBKLY"
keywd="MICHAEL"

def col_reader_spreader(text, keywd):
    lst=[]
    c=len(keywd)
    n=len(encoded)//c
    for i in range(n):
        lst.append(text[i::n])
    return lst

print(col_reader_spreader(encoded,keywd))


'''
"A"	0
"C"	1
"E"	2
"H"	3
"I"	4
"L"	5
"M"	6

M I C H A E L
6 4 1 3 0 2 5

H D E X Y A T
X E S S X T N
H X U Y L X S
E K X B K L Y

HXHE 
DEXK
ESUX
XSYB
YXLK
ATXL
TNSY

6413025
BUYTHES
KYANDSE
LLTHESK
YXXXXXX

HDEXYATXESSXTNHXUYLXSEKXBKLY



HALSX
4, 9, 14, 19, 24

YKSHX
2, 7, 12, 17, 22

TYEEX
3, 8, 13, 18, 23

BENLK
0, 5, 10, 15, 20

USDTY
1, 6, 11, 16, 21

'''