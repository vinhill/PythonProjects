#compute reversed complementary dna strand
dna = list(input('please enter the dna sequence: '))
rc = list()#reverse complement
for c in dna[::-1]:
    if c == 'A':
      rc.append('T')
    elif c == 'T':
      rc.append('A')
    elif c == 'C':
      rc.append('G')
    elif c == 'G':
      rc.append('C')
print("".join(rc))