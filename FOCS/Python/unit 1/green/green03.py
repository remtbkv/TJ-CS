def bool_myst_A(x):
    if x%2==0:
        return True
    if x%3==0:
        return True
    else:
        return False
    
def bool_myst_B(x):
    if x>=10:
        return True
    elif x%2==1:
        return False
    else: 
        return True

def bool_myst_C(x):
    if x%3==0:
        return False
    else:
        return True

def bool_myst_D(x):
  if x <= 3 or x>=10:
    return True
  else:
    return False

def bool_myst_E(x):
  if x%3==0 or x%5==0:
    return False
  else:
    return True

def bool_myst_F(x):
  if x<=4 or x>=10:
    return False
  else:
    return True

def date_fashion(you, date):
    if (you > 8 and you < 10) or (date > 8 and date < 10):
      return 2
    elif (you > 0 and you < 2) or (date > 0 and date < 2):
      return 0
    elif (you > 0 and you < 10) or (date > 0 and date < 10):
      return 1

def squirrel_play(temp, is_summer):
  if not is_summer and int(temp >= 60 and temp <= 90):
    return True
  elif is_summer and int(temp >= 60 and temp <= 100):
    return True
  else:
    return False

def caught_speeding(speed, is_birthday):
    if is_birthday and (speed >=66 and speed <=85):
        return 1
    elif not is_birthday and int(speed >=61 and speed <=80):
        return 1
    elif not is_birthday and int(speed <=60):
        return 0
    elif is_birthday and int(speed <= 65):
        return 0
    elif not is_birthday and int(speed >=81):
        return 2
    elif is_birthday and int(speed >=86):
        return 2

def sorta_sum(a, b):
    if (a + b) >= 10 and (a + b) <= 19:
        return 20
    else:
        return a+b

def alarm_clock(day, vacation):
  if day==6 and vacation==False or day==0 and vacation==False :
    return "10:00"
  elif int(day>=1 and day<=5 and vacation==False ):
    return "7:00"
  elif vacation and day==6 or vacation and day==0:
    return "off"
  elif day>=1 and day<=5 and vacation==True:
    return "10:00"

def love6(a, b):
    if a == 6 or b == 6:
        return True
    elif (a+b) == 6 or abs(a-b) == 6:
        return True
    else:
        return False

def in1to10(n, outside_mode):
    if (n <= 1 or n >= 10) and outside_mode == True:
        return True
    elif not outside_mode and n >= 1 and n <= 10:
        return True
    else:
      return False

def near_ten(num):
  if num % 10 ==0:
    return True
  elif num % 10 ==1:
    return True
  elif num % 10 ==2:
    return True
  elif abs(num % 10 - 10)>2:
    return False
  elif abs(num % 10 - 10)<=2:
    return True