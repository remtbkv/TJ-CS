snode = "ABCDEFGHIJKLMNO."
snode = ".ABCDEFGHIJKLMNO"
# snode = "ABCDEFGHIJKLMNOPQRSTUVWX." # 5x5
# snode = ".ABCDEFGHIJKLMNO" # korf
N, tdct, r_dct, c_dct = int(pow(len(snode), 0.5)), {}, {}, {}
# tdct = {'A': (0, 0), 'B': (0, 1), 'C': (0, 2), 'D': (0, 3),
#         'E': (1, 0), 'F': (1, 1), 'G': (1, 2), 'H': (1, 3),
#         'I': (2, 0), 'J': (2, 1), 'K': (2, 2), 'L': (2, 3),
#         'M': (3, 0), 'N': (3, 1), 'O': (3, 2), '.': (3, 3)}
i = 0
# for ind, val in enumerate(snode):
#     tdct[val] = (ind//N, ind%N)

tdct = {val: (ind//N, ind%N) for ind, val in enumerate(snode)}