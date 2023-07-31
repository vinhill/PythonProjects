from utils import FASTAReader
import numpy as np

def to_base_10(num, base):
    # convert number to base 10
    return sum([v * base**(len(num)-i-1) for i, v in enumerate(num)])

def numericalize(seq, alphabet):
    # convert characters to numbers
    return [alphabet.index(c) for c in seq]

def k_mer_composition(seq, k, alphabet):
    comp = np.zeros(shape=(len(alphabet)**k), dtype=int)
    nseq = numericalize(seq, alphabet)
    sz_alph = len(alphabet)

    kmer = to_base_10(nseq[:k], sz_alph)
    comp[kmer] += 1
    for i in range(4, len(seq)):
        # shift kmer to the left by 1
        kmer = (kmer % (sz_alph**(k-1))) * sz_alph + nseq[i]
        comp[kmer] += 1

    return comp

if __name__ == "__main__":
    reader = FASTAReader(input("path:" ))
    seq = reader.nextDNA()
    k = 4
    alphabet = "ACGT"
    comp = k_mer_composition(seq, k, alphabet)
    print(" ".join([str(c) for c in comp]))