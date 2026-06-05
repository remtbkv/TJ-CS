def mystery1(x):
  return x*-3

def mystery2(x):
  return x+7

def mystery3(x):
  return 2*x-1

def mystery4(x, y):
  return x-y

def mystery5(x):
  if x < 0:
    return x/2
  else:
    return 1000000

def mystery6(x):
  return x^2-2

def mystery7(x, y):
  if x > 0:
    return x
  else:
    return y
  
def mystery8(x):
  if (x % 2)==1:
    return 19
  else:
    return 0

def mystery9(x):
  if x % 2 ==1:
    return (x % 2)*-1
  else:
    return x*2

def mystery10(x, y):  
  if x > y:
    return x*5
  else:
    return y*5

def mystery11(x):
  if x % 2 ==1:
    return (x % 2)*x*3 + 1
  else:
    return x/2

def mystery12(x):
    return int(x/3)



# def maya(x):
#  if x == 1:
#    return 1
#  else:
#    return maya(x-1)*x