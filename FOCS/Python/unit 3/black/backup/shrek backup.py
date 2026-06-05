def printer(board):
    lst=list(board.values())
    print(lst)
    print(" " + "\n"+"-----------------------------")
    for i in range(7,50,7):
        print("| " + " | ".join(lst[i-7:i]) + " |" +"\n")
    print("-----------------------------")
    

# tent = [] # 13, 8
# tent1=random.choice(num)
# tent.append(tent1), num.remove(tent1)
# tent2=random.choice(num)
# tent.append(tent2), num.remove(tent2)

# mud = [] # 22, 5
# mud1=random.choice(num)
# mud.append(mud1),num.remove(mud1)
# mud2=random.choice(num)
# mud.append(mud2), num.remove(mud2)

# print()
# print("Shrek:",shrek)
# print("Tentacles:",tent)
# print("Mud:",mud)


# width=7
# height=7
# coordinates = [(x, y) for y in range(width) for x in range(height)] # inverted coordinate plane (you want this)


# def get_nested(data, *args):
#     if args and data:
#         element  = args[0]
#         if element:
#             value = data.get(element)
#             return value if len(args) == 1 else get_nested(value, *args[1:])


# dct={"foo":{"bar":{"one":1, "two":2}, "misc":[1,2,3]}, "foo2":123}
# get_nested(dct, "foo", "bar", "one")
# get_nested(dct, "foo", "bar", "two")
# get_nested(dct, "foo", "misc")
# get_nested(dct, "foo", "missing")


# nested={(0, 0): 0, 0: {"bats": 0, "mud": 0, "shrek": 0}, (1, 0): 0, 0: {"bats": 0, "mud": 0, "shrek": 0}, (2, 0): 0, 0: {"bats": 0, "mud": 0, "shrek": 0}, (3, 0): 0, 0: {"bats": 0, "mud": 0, "shrek": 0}, (4, 0): 0, 0: {"bats": 0, "mud": 0, "shrek": 0}, (5, 0): 0, 0: {"bats": 0, "mud": 0, "shrek": 0}, (6, 0): 0, 0: {"bats": 0, "mud": 0, "shrek": 0}, (0, 1): 0, 0: {"bats": 0, "mud": 0, "shrek": 0}, (1, 1): 0, 0: {"bats": 0, "mud": 0, "shrek": 0}, (2, 1): 0, 0: {"bats": 0, "mud": 0, "shrek": 0}, (3, 1): 0, 0: {"bats": 0, "mud": 0, "shrek": 0}, (4, 1): 0, 0: {"bats": 0, "mud": 0, "shrek": 0}, (5, 1): 0, 0: {"bats": 0, "mud": 0, "shrek": 0}, (6, 1): 0, 0: {"bats": 0, "mud": 0, "shrek": 0}, (0, 2): 0, 0: {"bats": 0, "mud": 0, "shrek": 0}, (1, 2): 0, 0: {"bats": 0, "mud": 0, "shrek": 0}, (2, 2): 0, 0: {"bats": 0, "mud": 0, "shrek": 0}, (3, 2): 0, 0: {"bats": 0, "mud": 0, "shrek": 0}, (4, 2): 0, 0: {"bats": 0, "mud": 0, "shrek": 0}, (5, 2): 0, 0: {"bats": 0, "mud": 0, "shrek": 0}, (6, 2): 0, 0: {"bats": 0, "mud": 0, "shrek": 0}, (0, 3): 0, 0: {"bats": 0, "mud": 0, "shrek": 0}, (1, 3): 0, 0: {"bats": 0, "mud": 0, "shrek": 0}, (2, 3): 0, 0: {"bats": 0, "mud": 0, "shrek": 0}, (3, 3): 0, 0: {"bats": 0, "mud": 0, "shrek": 0}, (4, 3): 0, 0: {"bats": 0, "mud": 0, "shrek": 0}, (5, 3): 0, 0: {"bats": 0, "mud": 0, "shrek": 0}, (6, 3): 0, 0: {"bats": 0, "mud": 0, "shrek": 0}, (0, 4): 0, 0: {"bats": 0, "mud": 0, "shrek": 0}, (1, 4): 0, 0: {"bats": 0, "mud": 0, "shrek": 0}, (2, 4): 0, 0: {"bats": 0, "mud": 0, "shrek": 0}, (3, 4): 0, 0: {"bats": 0, "mud": 0, "shrek": 0}, (4, 4): 0, 0: {"bats": 0, "mud": 0, "shrek": 0}, (5, 4): 0, 0: {"bats": 0, "mud": 0, "shrek": 0}, (6, 4): 0, 0: {"bats": 0, "mud": 0, "shrek": 0}, (0, 5): 0, 0: {"bats": 0, "mud": 0, "shrek": 0}, (1, 5): 0, 0: {"bats": 0, "mud": 0, "shrek": 0}, (2, 5): 0, 0: {"bats": 0, "mud": 0, "shrek": 0}, (3, 5): 0, 0: {"bats": 0, "mud": 0, "shrek": 0}, (4, 5): 0, 0: {"bats": 0, "mud": 0, "shrek": 0}, (5, 5): 0, 0: {"bats": 0, "mud": 0, "shrek": 0}, (6, 5): 0, 0: {"bats": 0, "mud": 0, "shrek": 0}, (0, 6): 0, 0: {"bats": 0, "mud": 0, "shrek": 0}, (1, 6): 0, 0: {"bats": 0, "mud": 0, "shrek": 0}, (2, 6): 0, 0: {"bats": 0, "mud": 0, "shrek": 0}, (3, 6): 0, 0: {"bats": 0, "mud": 0, "shrek": 0}, (4, 6): 0, 0: {"bats": 0, "mud": 0, "shrek": 0}, (5, 6): 0, 0: {"bats": 0, "mud": 0, "shrek": 0}, (6, 6): 0, 0: {"bats": 0, "mud": 0, "shrek": 0}}


# for i in coord:
#     print(i, nested.get(i),"|",nested[0]["bats"], nested[0]["mud"], nested[0]["shrek"])


# def frame(size=7):
    
#     upper = ("┌───┐ "*size) + "\n│   ├ " + ("┤   ├ "*(size-2)) + "┤   │\n" + ("└─┬─┘ "*size)
#     middle = ("┌─┴─┐ "*size) + "\n│   ├ " + ("┤   ├ "*(size-2)) + "┤   │\n" + ("└─┬─┘ "*size)
#     bottom = ("┌─┴─┐ "*size) + "\n│   ├ " + ("┤   ├ "*(size-2)) + "┤   │\n" + ("└───┘ "*size)
    
#     print(upper)
#     for i in range(size-2):
#         print(middle)
#     print(bottom)