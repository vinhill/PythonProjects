#compute the hamming distance between two strings
#we only look at how many symbols arent the same.
def ham_dist(s1, s2):
  d = 0
  for i in range(len(s1)):
    if s1[i] != s2[i]:
      d += 1
  return d

s1 = input("enter first string: ")
s2 = input("enter second string: ")
print(ham_dist(s1,s2))