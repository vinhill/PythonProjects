from utils import FASTAReader

def failure_arraz(seq):
    pass

if __name__ == "__main__":
    reader = FASTAReader(input("path: "))
    seq = reader.nextDNA()
    fail = failure_arraz(seq)
    print(" ".join([str(f) for f in fail]))