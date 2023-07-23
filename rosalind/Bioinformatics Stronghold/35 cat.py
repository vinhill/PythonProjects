from functools import lru_cache
from utils import FASTAReader

@lru_cache(maxsize=None)
def catalan(n):
    if n in (0, 1):
        return 1
    else:
        return sum(catalan(k-1) * catalan(n-k) for k in range(1,n+1))
    
def can_bond(b1, b2):
    return (b1+b2) in ("AU", "UA") or (b1+b2) in ("GC", "CG")

@lru_cache(maxsize=None)
def perfect_bonding_matchings(seq):
    if len(seq) in (0, 1):
        return 1
    else:
        sum = 0
        # ateps of two as both sides of {0, k} need to have even number of remaining nodes
        # so that perfect match is possible
        for k in range(1,len(seq),2):
            if can_bond(seq[0], seq[k]):
                sum += perfect_bonding_matchings(seq[1:k]) * perfect_bonding_matchings(seq[k+1:])
        return sum
    
def repstr(s, n):
    return "".join([s for _ in range(n)])

if __name__ == "__main__":
    for n in range(0,100):
        assert catalan(n) == perfect_bonding_matchings(repstr("AU", n)), f"{catalan(n)} != {perfect_bonding_matchings(repstr('AU', n))}"

    assert perfect_bonding_matchings("AUAU") == 2
    assert perfect_bonding_matchings("CGGCUGCUACGCGUAAGCCGGCUGCUACGCGUAAGC") % 1000000 == 736, perfect_bonding_matchings("CGGCUGCUACGCGUAAGCCGGCUGCUACGCGUAAGC")

    f = FASTAReader(input("path: "))
    seq = f.nextDNA()
    print(perfect_bonding_matchings(seq) % 1000000)