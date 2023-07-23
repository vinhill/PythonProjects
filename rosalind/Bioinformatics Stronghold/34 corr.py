from utils import FASTAReader, BioInfUtils, Trie
from itertools import product

class Read:
    def __init__(self, seq):
        self.seq = seq
        self.comp = BioInfUtils.reverseComplement(seq)
        self.normalized = self.seq if self.seq < self.comp else self.comp

    def __eq__(self, other):
        return self.normalized == other.normalized

    def __hash__(self):
        return hash(self.normalized)
    
    def __repr__(self):
        return self.normalized
    
    def __str__(self):
        return self.normalized
    
    def change(self, i, c):
        read = list(self.seq)
        read[i] = c
        return Read("".join(read))
    
def hamming_dist(s1, s2):
    assert len(s1) == len(s2)
    return sum(c1 != c2 for c1, c2 in zip(s1, s2))

reads = [dna for _, dna in FASTAReader(input("path: "))]
reads = list(map(Read, reads))
reads.sort(key=lambda r: r.normalized)

unique_reads = set()
correct_reads = set()
for i, read in enumerate(reads):
    if i-1 >= 0 and reads[i-1] == read:
        correct_reads.add(read)
    elif i+1 < len(reads) and reads[i+1] == read:
        correct_reads.add(read)
    else:
        unique_reads.add(read)

creads_trie = Trie()
for cread in correct_reads:
    creads_trie.add(cread.normalized, cread)

for uread in unique_reads:
    seq = uread.normalized
    for i, c in product(range(len(seq)), ('A', 'T', 'C', 'G')):
        read = uread.change(i, c)
        n = creads_trie.walk(read.normalized)
        if n != None:
            print(uread.seq, end="")
            print("->", end="")
            print(n.get().seq)
            break
    else:
        print(uread)
        for read in reads:
            if id(read) == id(uread): continue
            if read.seq == uread.seq or read.comp == uread.seq:
                print(read)
                print("Should've been correct read")
            if hamming_dist(read.seq, seq) == 1 or hamming_dist(read.comp, seq) == 1:
                print(read)
                print("Found a match but not via trie")
                print(creads_trie.walk(read.normalized))
        print("Error, exiting.")
        exit()