#3 Overlap Graph
from utils import FASTAReader

k = 3
fasta = FASTAReader("12 grph.txt")
dna_list = fasta.remainingList()

for id, dna in dna_list:
  for id2, dna2 in dna_list:
    if id == id2:
      continue
    if dna2.startswith(dna[len(dna)-k:]):
      print(id + " " + id2)