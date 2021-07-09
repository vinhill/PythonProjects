#fragment assembly
"""
Probably not always finding the shortest superstring
"""
from utils import FASTAReader

strands = FASTAReader("25 long.txt").remainingDNAList()
res = strands[0]
strands = strands[1:]

while len(strands) > 0:
    max_overlap = 0
    max_s = ""
    for s in strands:
        for i in range(1,len(s)):
            if ( s[0:i] == res[-i:] or s[-i:] == res[0:i] ) and i > max_overlap:
                max_overlap = i
                max_s = s
    strands.remove(max_s)
    if max_s[0:max_overlap] == res[-max_overlap:]:
        res = res + max_s[max_overlap:]
    else:
        res = max_s + res[max_overlap:]
print(res)