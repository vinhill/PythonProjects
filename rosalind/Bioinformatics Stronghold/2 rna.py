#compute rna from dna
import re
dna = 'AGCCCATTCCTAGCTGGACTCCATCTACGCTGGACACTTGGGGGAGAGCTGATCGGCCAAACCTGGCCACGACCTTGTTCTGTATATTTTTTGTGGAGAGAAGGCGCACCTAGAACGGTGACGACATTTTTACGGCACGAGGATGGTAGCGAACGTCGTTCCTATGACATAGAATGATCCCTGCATGAGAGCTCAATGGTTCACAAAAATCAGAATGTTGGTAAACACTACGCTCGTGCTTCGCGGTCCCACAAGAATAAGTGGCAGCTACACACTTCGGCCAAGACGGATAGTTGATGTCAGGCTAAGTCAATACGAGGTGTCGCGATCTCAGGTGAAGCCCATGGTTTCTCATATAGGTATCTCCCCTGATTATCTAGACGCAAATTCGGACGCCAGGCAAAGATCAGAGATGTAGTTAACGGTGCTGTGTTTAACACTACACCGCTTCGGGGCTAGGCATAAAATGACGGCCAGCCTTAAGTCAGCAAACGGGTCAATTTGGATGGGCGTGTTCGCTCCTTTTATGGGTAGGATATCCGGGCTCGGATGTAACGCTGACATCTAAACATTTGGGTAGGGACCCCATTAAACCTTAGGGCTTGAACCATAGCGTACCGGCGGATAGGAGATCCATCGACTGTCACTGAGGGCTAGTTCGCTCCCAGAAAAAACAGTCACATTGCCATGGTCGTAAGAGGGGCCTTAGACCATTGCCTGCCCTCGAAAAACCCCCGATCAACTGTAAGTGACGCATACGTACGGATGTAACCAATTCTGCAAGCAACAACGTGAGAACTCTCCCCAGTAATCTTCCCAGTATGCTTTGACCACAATCGGAGAGCCCTAGGGTGTTCTCCTGTGGCAAGGGTGATGTGACCCATCTTCGGTTGCTTGGCTGTATCGAACAC'
print(re.sub('T','U',dna))