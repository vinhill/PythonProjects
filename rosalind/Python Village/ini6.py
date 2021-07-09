#list how often each word occurs
f = open("ini6.txt")

woc = {} #word occurency count

for line in f:
    words = line.replace('\n', '').split(' ')
    for w in words:
        if w in woc:
            woc[w] = woc[w]+1
        else:
            woc[w]=1

for k,v in woc.items():
    print("{word} {count}".format(word = k, count = v))

f.close()