def malcolm(m):
  return 2*m + 1

def elaisa(x, y):
  return 2*x-y

def akash(b):
  if b > 0:
    return 1
  else:
    return -1

def rosa(r):
  return ((r-1)*2 + 1)*-1

def aashni(n):
  return akash(n)*n

def dion(d):
  if d > 10:
    return malcolm(d)
  else:
    return rosa(d)

def zhixing(a, b):
  return (elaisa((aashni(a)), (rosa(b))))*2