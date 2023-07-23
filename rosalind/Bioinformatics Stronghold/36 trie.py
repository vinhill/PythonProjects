from utils import Trie

def print_adj_list(lbl, u):
    thislabel = lbl
    lbl += 1
    for e in u.children:
        print(f"{thislabel} {lbl} {e}")
        lbl = print_adj_list(lbl, u.children[e])
    return lbl

if __name__ == "__main__":
    with open(input("path: ")) as f:
        seqs = f.readlines()

    #seqs = ["ATAGA", "ATC", "GAT"]

    t = Trie()
    for seq in seqs:
        t.add(seq.strip(), seq)
    
    print_adj_list(1, t)