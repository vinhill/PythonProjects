from utils import FASTAReader

fasta = FASTAReader("14 lcsm.txt")
first = fasta.nextDNA()
rest = fasta.remainingDNAList()

max_i = 0
max_j = 0
for i in range(len(first)):
  for j in range(i+max_j-max_i+1,len(first)):
    if all( first[i:j] in x for x in rest ):
      max_j = j
      max_i = i

print(first[max_i:max_j])