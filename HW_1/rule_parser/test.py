to = [(9, 11)]
fro = [(0, 1), (1, 2), (3, 4), (4, 5), (5, 6), (9, 10), (10, 11), (11, 12), (12, 13), (13, 14), (14, 15), (15, 16), (16, 17), (17, 18), (18, 19), (20, 21)]

import itertools

def intersect(input_list1, input_list2):
    out_ranges = []
    for i, j in input_list2:
        out_ranges.append([*range(i, j+1)])
    out_ranges = [item for sublist in out_ranges for item in sublist]
    final = []

    for i, j in input_list1:
        flag = False
        for el in range(i, j):
            if el in out_ranges:
                flag = True
        if flag:
            final.append((i,j))

    return final



print(intersect(fro, to))