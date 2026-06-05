s = input("Please type a string: ")
print("#1: ", s[2])
print("#2: ",s[4])
print("#3: ",len(s))
print("#4: ",s[0])
print("#5: ",s[-1])
print("#6: ",s[-2])
print("#7: ",s[3:8])
print("#8: ",s[8:])
print("#9: ",s[3:])
print("#10: ",s.lower())
print("#11: ",s.upper())
print("#12: ",list(s))
print("#13: ",s[:-1])
print("#14: ",s[1:])
c="e"
d="E"
print("#15: ",s.count(c))
print("#16: ",s.count(c)+s.count(d))
lst=[]
for v in s:
    if v in ["a","e","i","o","u","A","E","I","O","U"]:
        lst.append(v)
print("#17: ",len(lst))
print("#18: ",lst)
print("#19: ",s[::2])
print("#20: ",s[1::2])
x=2
print("#21: ",[s[i:i+x] for i in range(len(s)-1)])
ll=[]
for count, letter in enumerate(s):
    if count%3==0:
        ll.append("!")
    else:
        ll.append(letter)
print("#22: ","".join(ll))
lll=[]
for count, letter in enumerate(s, start=1):
    if count%3==0:
        lll.append("!")
    else:
        lll.append(letter)
print("#23: ","".join(lll))