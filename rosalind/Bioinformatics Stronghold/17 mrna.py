from utils import BioInfUtils

aas = input("enter amino accid sequence: ") + "s"
codon_dict = BioInfUtils.getCodonDict()

res = 1
for aa in aas:
    res = res * len(list(filter(lambda kv: kv[1] == aa, codon_dict.items()))) % 1000000
print(res)