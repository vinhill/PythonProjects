from utils import Utils
k=7
n=35
print(1 - Utils.binom_cdf(2**k,n-1,0.25))
"""
This solution works, but I dont agree with it.
It assumes a organism lives only one generation
Looking at the task, it should be 3**k as after mating the individuum continues to live
"""