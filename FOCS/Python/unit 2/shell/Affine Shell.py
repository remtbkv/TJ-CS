# This file contains some global variables, imports, functions and test cases you'll need for assignment 02-04!

# First: the necessaries.  Copy/paste these lines of code to be at the top of your affine file, above all of your
# function definitions.  Explanations for what's going on here are in the videos if you need to refer back!

import math

alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def mod_inverse_helper(a, b):
    q, r = a//b, a%b
    if r == 1:
        return (1, -1 * q)
    u, v = mod_inverse_helper(b, r)
    return (v, -1 * q * v + u)

def mod_inverse(a, m):
    assert math.gcd(a, m) == 1, "You're trying to invert " + str(a) + " in mod " + str(m) + " and that doesn't work!"
    return mod_inverse_helper(m, a)[1] % m

# Now: test cases.  These test cases come in two blocks.  Copy/paste and uncomment each block when you finish that
# part of the assignment.



# Part 1: test your affine_encode and affine_decode.
# When you run these lines, the output should be EXACTLY this:
# WMDNZPXVUQHFEGHISZBKDAHCDQWMDYROLAHJ THEQUICKBROWNFOXJUMPEDOVERTHELAZYDOG
#
# text = "THEQUICKBROWNFOXJUMPEDOVERTHELAZYDOG"
# enc = affine_encode(text, 3, 17)
# dec = affine_decode(enc, 3, 17)
# print(enc, dec)



# Part 2: test your affine_n_encode and affine_n_decode.
# When you run these lines, the output should be EXACTLY this:
# USLTFZITNPBJEWREMCQTPQONLCWPJAFFGWWHPZFG THEQUICKBROWNFOXJUMPEDOVERTHELAZYDOGXXXX
#
# text = "THEQUICKBROWNFOXJUMPEDOVERTHELAZYDOG"
# enc = affine_n_encode(text, 5, 347, 1721)
# dec = affine_n_decode(enc, 5, 347, 1721)
# print(enc, dec)



# Get Your Code Ready to Turn In
# 1) Delete or comment out all previous test cases
# 2) Uncomment this code and add it to the bottom of your file!
#
# import sys
# text, dec1, dec2 = sys.argv[1:4]
# a, b, n, n_a, n_b = [int(x) for x in sys.argv[4:]]
# print(affine_encode(text, a, b))
# print(affine_decode(dec1, a, b))
# print(affine_n_encode(text, n, n_a, n_b))
# print(affine_n_decode(dec2, n, n_a, n_b))