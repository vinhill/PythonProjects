with open(input("path: ")) as f:
    n = int(f.readline())
    edges = f.readlines()

print(n-len(edges)-1)