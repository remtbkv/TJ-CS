'''
1. cookie_cutter(a-1, b, c, d) is the recursive value
2. the value of B controls when the recursion stops
3. the value of C sets the base case return value
4. the value of D modifies the base case return value by being multiplied each time the function recurs
5. cookie_cutter(5, 0, 1, 2) returns:

2 * (4)
2 * (2 * (3))
2 * 2 * (2 * (2))
2 * 2 * 2 * (2 * (1))
2 * 2 * 2 * 2 * (2 *(0)) (0) = 1
2 * 2 * 2 * 2 * 2 * 1
=32

'''
def sum_arithmetic(n_terms, start_val, inc_val):
    final_term = start_val + (n_terms-1)*inc_val
    if n_terms==1:
        return start_val
    else:
        return final_term + sum_arithmetic(n_terms-1, start_val, inc_val)

def sum_geometric(n_terms, start_val, mult_val):
    final_term = start_val * (mult_val**(n_terms-1))
    if n_terms==1:
        return start_val
    else:
        return final_term + sum_geometric(n_terms-1, start_val, mult_val)

import sys
a = float(sys.argv[1])
b = float(sys.argv[2])
c = float(sys.argv[3])
print(sum_arithmetic(a, b, c))
print(sum_geometric(a, b, c))