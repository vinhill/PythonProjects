f = open("ini5.txt")
even = False
for line in f:
    if(even):
        print(line, end='')
        even = False
    else:
        even = True