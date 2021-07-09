#reverse palindrome of length 4-12 (inclusive)
from utils import FASTAReader, BioInfUtils

dna = FASTAReader("21 revp.txt").nextDNA()

for i in range(len(dna)-3):
    for j in range(i+4, min(i+12,len(dna))+1):
        if dna[i:j] == BioInfUtils.reverseComplement(dna[i:j]):
            print("{0} {1}".format(i+1, j-i))