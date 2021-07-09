#print all partitions of {1,...,n}
import itertools
from functools import reduce

n = int(input("enter n: "))

print(reduce(lambda x, y: x*y, range(1,n+1),1))

for p in itertools.permutations(list(range(1,n+1))):
    print(str(p)[1:-1].replace(",",""))