alphabet = "A B C D".split()
k = len(alphabet)
n = 4

for i in range(k**n):
    str = list()
    for j in range(n-1,-1,-1):
        str.append(alphabet[int(i / k**j)])
        i = i % k**j
    print("".join(str))