import sys
file = sys.argv[1]

import math

float_list=[]

with open(file) as f:
    for i in f:
        float_list.append(float(i))

sorted=(sorted(float_list))

n=len(sorted)
q1_o=((n+1)//4)
q1_e=math.ceil(((n/2)+1)/2)
m=math.ceil(n/2)
mm=int((n+1)/2)
temp=[]
for i in sorted:
    temp.append(i)


print("Average:",sum(temp)/n)

print("Min:",min(sorted))

if n%2==1:
    print("Q1:",(sorted[q1_o]+sorted[q1_o-1])/2) # q1
    print("Median",sorted[m-1]) # med
    print("Q3:",(sorted[m-1:][q1_o-1]+sorted[m-1:][q1_o])/2) #q3
elif n%2==0:
    print("Q1",(sorted[:mm][q1_e-1]+sorted[:mm][q1_e-2])/2) # q1
    print("Median:",(sorted[m-1]+sorted[m])/2) #med
    print("Q3",(sorted[mm-1:][q1_e-1]+sorted[mm-1:][q1_e])/2) #q3

print("Max:",max(sorted))





