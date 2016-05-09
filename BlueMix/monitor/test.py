# x = 630;
# count = 0;
# while(x != 0):
#     d = x % 10
#     x = x/10
#     if d == 0 or d == 4 or d == 6 or d == 9:
#         

import itertools
somelists = [
   [1, 1, 2, 3],
   ['a', 'b'],
   [4, 5]
]
for element in itertools.product(*somelists, repeat=1):
    print element