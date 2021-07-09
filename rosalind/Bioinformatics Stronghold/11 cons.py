#generate an average strand
from utils import FASTAReader

fasta = FASTAReader("11 cons.txt")

id, dna = fasta.next()
dna_len = len(dna)
profile = dict()
for i in range(dna_len):
  profile[('A',i)]=0
  profile[('G',i)]=0
  profile[('C',i)]=0
  profile[('T',i)]=0

fasta.reset()
for id, dna in fasta:
  for i in range(dna_len):
    profile[(dna[i],i)] = profile[(dna[i],i)] + 1

avg_dna = list()
for i in range(dna_len):
  cmax = 'A'
  max = profile[('A',i)]
  for c in ['C','G','T']:
    if profile[(c,i)] > max:
      cmax = c
      max = profile[(c,i)]
  avg_dna.append(cmax)

print("".join(avg_dna))

for c in ["A","C","G","T"]:
  print(c + ": ", end="")
  for i in range(dna_len):
    print(str(profile[(c,i)]) + " ", end="")
  print()