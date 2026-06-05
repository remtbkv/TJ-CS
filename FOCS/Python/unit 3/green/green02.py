import sys
file = sys.argv[1]

dates=[]

with open(file) as f:
    for i in f:
        dates.append(i.strip())

converted=[]

for i in dates:
    if "-" in i:
        converted.append(i)

    elif "/" in i:
        temp=[]
        if int(i[0])<10 and i[1]=="/":
            temp.append("0"+str(i))
        else:
            temp.append(str(i))
        
        replaced=[]
        for i in temp:
            replaced.append(i.replace("/","-"))

        for i in replaced:
            if i[4]=="-":
                l=list(i)
                l.insert(3,"0")
                l.insert(0, "".join(l[6:]))
                del l[6:]
                l.insert(1,"-")
                if int("".join(l[0]))<100 and int("".join(l[0]))>21 : 
                    l.insert(0,"19")
                else:
                    l.insert(0,"20")
                converted.append("".join(l))

            else:
                temp=[]
                temp.append(i[-2:])
                temp.insert(2,"-")
                temp.append(i[:-3])
                if int("".join(temp[0]))<100 and int("".join(temp[0]))>21 : 
                    temp.insert(0,"19")
                else:
                    temp.insert(0,"20")
                converted.append("".join(temp))
            
    elif "," in i:
        dict={"January": "01", "February": "02", "March": "03", "April": "04", "May": "05", "June": "06", "July": "07", "August": "08", "September": "09", "October": "10", "November": "11", "December": "12"}
        
        
        if i[-8]==" ":
            s=list(i)
            s.insert(-7, "0")
            ss=list(i[-2:]+"--"+"".join(s[-8:-6]))
            month="".join(s[:-9])
            ss.insert(3, dict.get(month))
            if int("".join(ss[0:2]))<100 and int("".join(ss[0:2]))>21: 
                ss.insert(0,"19")
            else:
                ss.insert(0,"20")
            converted.append("".join(ss))
        else:
            dict={"January": "01", "February": "02", "March": "03", "April": "04", "May": "05", "June": "06", "July": "07", "August": "08", "September": "09", "October": "10", "November": "11", "December": "12"}

            temp=[]
            s=list(i)
            temp.append("".join(s[-2:]))
            temp.append(dict.get("".join(s[:-9])))
            temp.append("".join(s[-8:-6]))
            ss=list("-".join(temp))
            if int("".join(ss[0:2]))<100 and int("".join(ss[0:2]))>21:
                ss.insert(0,"19")
            else:
                ss.insert(0,"20")
            converted.append("".join(ss))

sorted = sorted(converted)
n=0

with open("sorted_dates.txt", "w") as g:
    for i in range(len(sorted)-1):
        g.write(sorted[i]+"\n")
    g.write(sorted[-1])

