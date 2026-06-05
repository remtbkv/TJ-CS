import sys

if sys.argv[1]=="A":
    print(int(sys.argv[2]) + int(sys.argv[3]) + int(sys.argv[4]))
elif sys.argv[1]=="B":
    print(sum([int(i) for i in sys.argv[2:]]))
elif sys.argv[1]=="C":
    print([int(i) for i in sys.argv[2:] if int(i)%3==0])
elif sys.argv[1]=="D":
    fib = lambda x: 1 if x<=2 else fib(x-2) + fib(x-1)
    print(" ".join([str(fib(i)) for i in range(1, int(sys.argv[2])+1)]))
elif sys.argv[1]=="E":
    print(" ".join([str(i**2-3*i+2) for i in range(int(sys.argv[2]), int(sys.argv[3])+1)]))
elif sys.argv[1]=="F":
    a, b, c = float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4])
    s = (a+b+c)/2
    if (-a+b+c)*(a-b+c)*(a+b-c)>0:
        print(((s*(s-a)*(s-b)*(s-c)))**0.5)
    else:
        print("Not a triangle")
elif sys.argv[1]=="G":
    print("\n".join(i+": "+str(sys.argv[2].count(i)) for i in "aeiou"))