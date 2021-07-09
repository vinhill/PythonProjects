#P(n,k)=n!/(n-k)!
import math
from functools import reduce
n = 97
k = 8
m=1000000
print(reduce(lambda a,b: a*b%m, range(n-k+1,n+1)))