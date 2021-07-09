#Find motif N{P}[ST]{P} in uniprot ids
from utils import BioInfUtils
import re

uniprot_ids = input("Please enter the uniprot_ids separated by space: ").split(" ")
motif = r"(?=N[^P][ST][^P])"

for id in uniprot_ids:
    dna = BioInfUtils.getUniprotFASTA(id)["dna"]
    if re.search(motif, dna):
        print(id)
        for m in re.finditer(motif, dna):
            print(str(m.start()+1) + " ", end="")
        print()