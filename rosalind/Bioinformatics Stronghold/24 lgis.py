import random
import numpy as np
from utils import Utils

def LOS_n2(perm, comp):
    prev = [None] * len(perm)
    leng = [1] * len(perm)

    for i, v in enumerate(perm):
        for j in range(i):
            if comp(perm[j], v) and leng[j] + 1 > leng[i]:
                leng[i] = leng[j] + 1
                prev[i] = j

    longest_start_idx = np.argmax(leng)
    longest_len = leng[longest_start_idx]
    
    seq = []
    i = longest_start_idx
    while i is not None:
        seq.append(perm[i])
        i = prev[i]
    seq.reverse()

    assert longest_len == len(seq)
    for i in range(1, len(seq)):
        assert comp(seq[i-1], seq[i])

    return seq

def LIS_patience(perm):
    pilestop = []
    prevtop = [None] * len(perm)
    for i, _ in enumerate(perm):
        j = Utils.lower_bound(pilestop, i, lambda e, v: perm[e] >= perm[v])
        if j == len(pilestop):
            pilestop.append(i)
        else:
            pilestop[j] = i
        prevtop[i] = pilestop[j-1] if j > 0 else None

    longest_start_idx = pilestop[-1]
    longest_len = len(pilestop)

    seq = []
    i = longest_start_idx
    while i is not None:
        seq.append(perm[i])
        i = prevtop[i]
    seq.reverse()

    assert longest_len == len(seq)
    for i in range(1, len(seq)):
        assert seq[i-1] < seq[i]
    
    return seq

def print_seq(seq):
    print(" ".join(map(str, seq)))

def test_n2():
    def equals(x, y):
        assert x == y, "{} != {}".format(x, y)
    less = lambda x,y: x < y
    greater = lambda x,y: x > y
    f = LOS_n2

    equals(f([1,2,3,4,5], less), [1,2,3,4,5])
    equals(f([0, -1, 1, -2, 2, -3, 3], less), [0, 1, 2, 3])
    equals(f([1, 0, -1, -2, 2, -3, 3], less), [1, 2, 3])
    equals(f([1, 5, 6, 2, 3, 4, 5], less), [1, 2, 3, 4, 5])
    seq = [0, 8, 4, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11, 7, 15]
    equals(len(f(seq, less)), len([0, 2, 5, 9, 11, 15]))
    seq.reverse()
    equals(len(f(seq, greater)), len([0, 2, 5, 9, 11, 15]))

def test_patience():
    def equals(x, y):
        assert x == y, "{} != {}".format(x, y)
    less = lambda x,y: x < y
    greater = lambda x,y: x > y
    f = LIS_patience

    equals(f([1,2,3,4,5]), [1,2,3,4,5])
    equals(f([0, 0, 1, 0, 2, 0, 3]), [0, 1, 2, 3])
    equals(f([1, 0, 0, 0, 2, 0, 3]), [0, 2, 3])
    equals(f([1, 5, 6, 2, 3, 4, 5]), [1, 2, 3, 4, 5])
    seq = [0, 8, 4, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11, 7, 15]
    equals(len(f(seq)), len([0, 2, 5, 9, 11, 15]))

if __name__ == "__main__":
    DEBUG = False
    
    if DEBUG:
        test_n2()
        test_patience()

    with open(input("path: ")) as f:
        n = int(f.readline())
        perm = list(map(int, f.readline().split()))
    
    assert len(perm) == n, "expected {} elements, got {}".format(n, len(perm))

    incr = LIS_patience(perm)
    decr = LIS_patience(perm[::-1])[::-1]
    
    if DEBUG:
        assert len(incr) == len(LOS_n2(perm, lambda x,y: x<y))
        assert len(decr) == len(LOS_n2(perm, lambda x,y: x>y))

    print_seq(incr)
    print_seq(decr)