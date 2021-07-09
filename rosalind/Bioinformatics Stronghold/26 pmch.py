import math
dna = "GUGCACCCAUAGGACCCUAGGAGGUUCGCCUGGUUACAACCGGGCCUGAGUUGAUCAGCAGGGUAGAGCUGACUCCCCUC"
gc = dna.count("G") + dna.count("C")
au = len(dna)-gc
print(math.factorial(gc//2) * math.factorial(au//2))