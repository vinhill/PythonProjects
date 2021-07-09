from itertools import permutations, product
from math import factorial
n = 5
f = open("out.txt", "w")
#there are n! permutations
#each symbol can be - or +
#therefore there are n! * 2**n signed permutations
f.write(str(factorial(n) * 2**n) + "\n")
#now list them
for p in permutations(range(1,n+1)):#[pi(1),pi(2),...]
    for i in range(2**n):
        A=bin(i)[2:]
        while(len(A)<n):
            A = "0" + A
        B=list(map(lambda x: x[0] if x[1] == "0" else -1*x[0], zip(p,A)))
        f.write(str(B).replace("[","").replace("]","").replace(",","") + "\n")
f.close()