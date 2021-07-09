from functools import reduce
from operator import mul
import math

dna="GATTAGCCATATAGAGCGTATGTTACACTGTTAACGGGCCCTAGCAGTGTTAGGCGGATCCCGATCAGCAATGTACTGACTCCACTAACGCTTCACAG"
A=map(float,"0.088 0.175 0.201 0.269 0.345 0.434 0.477 0.503 0.583 0.643 0.695 0.777 0.817 0.884".split())

#probability for char c given gc content x
def prob(c,x):
    if c in "GC":
        return x/2
    else:
        return (1-x)/2

B=map(lambda x: reduce(mul,map(lambda c: prob(c,x),dna)),A)
#format like in the example
s=str(list(map(lambda x: round(math.log10(x),3), B)))
print(s.replace("[","").replace(",","").replace("]",""))