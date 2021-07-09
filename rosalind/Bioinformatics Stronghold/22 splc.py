from utils import FASTAReader, BioInfUtils

introns = FASTAReader("22 splc.txt").remainingDNAList()
dna = introns[0]
introns = introns[1:]


for intron in introns:
    dna = dna.replace(intron, "")

print(BioInfUtils.rnaToAAS(dna.replace("T","U")))