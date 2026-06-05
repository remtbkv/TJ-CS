def mirror(s, x=0):
    if x == len(s):
        return s
    else:
        return s[len(s) - 1 - x] + mirror(s, x + 1)


def big_arch(s, x=1):
    if x == 1:
        print(s[0] + s + s[0])
    if x == len(s):
        return
    print(s[x] + " " * (len(s)) + s[x])
    big_arch(s, x + 1)


def weird_top(s, x=0, y=0):
    if x == (2 * len(s)):
        return
    l = len(s)
    l_m = s[(l - 1 - y)]
    small = (" " * x)
    big = (" " * (((l * 2) - 1) - x))
    print(small + l_m + big + l_m + big + l_m)
    weird_top(s, x + 2, y + 1)


def weird_bottom(s, x=2, y=0):
    l = len(s) * 2
    if x == (l + 2):
        return
    big = (" " * (l - x))
    small = (" " * (x - 1))
    print(big + s[y] + small + s[y] + small + s[y])
    weird_bottom(s, x + 2, y + 1)


def line(s, x=0):
    l = len(s)
    if x == l:
        return ""
    else:
        return s[l - 1 - x] + line(s, x + 1)


def star(s):
    weird_top(s)
    print(" ".join(line(s)) + " * " + " ".join(s))
    weird_bottom(s)


def word_art_11(s, x=0, y=0):  # spiral cube
    l = len(s)
    if x == 0:
        print(" ".join(s))
        word_art_11(s, x + 1, y + 1)
    elif x != 0 and x < l - 1:
        print(s[x] + " *" * (l - 2) + " " + s[l - 1 - y])
        word_art_11(s, x + 1, y + 1)
    elif x == l - 1:
        print(" ".join(s[::-1]))


def word_art_12(s, x=0, y=0):  # heart
    rev = s[::-1]
    rev_c = rev[1:-2]
    sp_rc = (" " * len(rev_c))

    if len(s) == 3 and x == 0:
        print(" " + s[1] + " " + s[1])
        word_art_12(s, x + 1)

    elif len(s) == 4 and x == 0:
        print(" " + s[1:3] + " " + s[1:3])
        word_art_12(s, x + 1)

    elif len(s) < 5 and x == 1:
        s_src = " " * (len(s) // 2)
        print(s[-1] + s_src + s[0] + s_src + s[-1])
        word_art_12(s, x + 1, y + 1)

    elif len(s) > 4 and x == 0:
        print(" " + rev_c + "   " + rev_c[::-1])
        word_art_12(s, x + 1)

    elif len(s) > 4 and x == 1:
        alt = (s[1] + s[0] + s[1])
        print(s[-1] + sp_rc + alt + sp_rc + s[-1])
        word_art_12(s, x + 1, y + 1)

    elif x > 1 and x < len(s):
        small = " " * y
        big = " " * ((len(s) * 2) - 2 - y - x)
        print(small + s[(len(s) - x)] + big + s[(len(s) - x)])
        word_art_12(s, x + 1, y + 1)

    elif x == len(s):
        print(" " * y + s[0])

word_art_12("awesome")

# import sys
# s = sys.argv[1]
# print("Mirror:")
# print()
# mirror(s)
# print()
# print("Big Arch:")
# print()
# big_arch(s)
# print()
# print("Star:")
# print()
# star(s)
# print()
# print("Spiral Cube:")
# print()
# word_art_11(s)
# print()
# print("Heart:")
# print()
# word_art_12(s)
