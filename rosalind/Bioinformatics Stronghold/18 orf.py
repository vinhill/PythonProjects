from utils import FASTAReader, BioInfUtils
import re

dna = FASTAReader("18 orf.txt").nextDNA()
rna1 = BioInfUtils.reverseComplement(dna).replace("T", "U")
rna2 = dna.replace("T", "U")

candidates = list()

for rna in [rna1, rna2]:
    i = rna.find("AUG")
    while i >= 0:
        for j in range(i+3,len(rna),3):
            if any(x == rna[j:j+3] for x in "UAA UAG UGA".split(" ")):
                candidate = BioInfUtils.rnaToAAS(rna[i:j])
                if candidate not in candidates:
                    candidates.append(candidate)
                break;
        i = rna.find("AUG", i+1)

for c in candidates:
    print(c)