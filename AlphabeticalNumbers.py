import math
from functools import reduce

exceptions = dict(map(
        lambda x: x.split(":"),
        "2x:twenty 3x:thirty 8x:eighty 10:ten 11:eleven 12:twelve 13:thirteen 14:fourteen 15:fiveteen 16:sixteen 17:seventeen 18:eighteen 19:nineteen".split()))
ones = "zero one two three four five six seven eight nine".split()
suffix = """
hundred thousand million billion 
trillion quadrillion quintillion hextillion septillion octillion nonillion 
decillion undecillion duodecillion tredecillion quattuordecillion quindecillion hexdecillion septendecillion octodecillion novemdecillion 
vigintillion unvigintillion duovigintillion trevigintillion quattourvigintillion quinvigintillion hexvigintillion septenvigintillion octovigintillion novemvigintillion 
triggintillion untrigintillion duotrigintillion
""".split()#counts till googol (exclusive) e.g. 10**100

def numToStr(number):
    if(number == 0):
        return "zero"
    #turn integer 123 into string representation "123"
    strrep = list()
    while(number > 0):
        strrep.append( number % 10 )
        number = math.floor(number / 10)
    strrep.reverse()
    #split strrep into groups of three numbers
    groups = list()
    i = len(strrep)
    while( i > 0 ):
        groups.append(strrep[max(0,i-3):i])
        i -= 3
    #fill up last group with 0
    groups[-1].reverse()
    if(len(groups[-1]) != 3):
        groups[-1].append(0)
    if(len(groups[-1]) != 3):
        groups[-1].append(0)
    groups[-1].reverse()
    #turn groups into text
    res = ""
    for i in range(0, len(groups)):
        if(i != 0):
            res = _tripleToStr(groups[i]) + suffix[i] + "-" + res
        else:
            res = _tripleToStr(groups[i]) + res
    return res
    
def _tripleToStr(triple):
    tripstr = "".join(map(lambda x: str(x), triple))
    res = ""
    #add x hundred
    if(triple[0] != 0):
        res = ones[triple[0]] + "hundred"
    #check for two digit exceptions (10,11,12)
    if(exceptions.get(tripstr[0:2])):
        res = res + exceptions.get(tripstr[0:2])
    #add y ty z
    else:
        #check for position 1 exceptions
        if(exceptions.get(tripstr[1] + "x")):
            res = res + exceptions.get(tripstr[1]+"x")
        elif(triple[1] != 0):
            res = res + ones[triple[1]] + "ty"
        if(triple[2] != 0):
            res = res + ones[triple[2]]
    return res