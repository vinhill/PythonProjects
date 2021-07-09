#calculate P(offspring has dominant allele) for k homozygous dominant, m heterozygous, n homozygous recessive
import random as rd

print("Please enter the given values.")
k,m,n = int(input("k: ")), int(input("m: ")), int(input("n: "))
s = ("k"*k) + ("m"*m) + ("n"*n)
count = 0
for i in range(10**7):
  r1, r2 = 0,0
  while r1 == r2:
    r1 = rd.randint(0, len(s)-1)
    r2 = rd.randint(0, len(s)-1)
  if s[r1] == 'k' or s[r2] == 'k':
    count += 1
  elif s[r1] == 'm' and s[r2] == 'm':
    count = count + 1 if rd.randint(1,4) != 4 else count
  elif s[r1] == 'm' or s[r2] == 'm':
    count = count + 1 if rd.randint(1,2) == 2 else count
print(count / (10**7))
print(count)