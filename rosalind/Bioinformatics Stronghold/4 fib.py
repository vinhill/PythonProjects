#rabbit reproduction simulation
def fib(n,k):
  assert n<=40 and k <= 5 and n>=0 and k >= 0, "n: {0} k: {1}".format(n,k)
  if n <= 2:
    return 1
  return fib(n-1,k)+k*fib(n-2,k)

n = int(input("months: "))
k = int(input("litter size: "))

print(fib(n,k))