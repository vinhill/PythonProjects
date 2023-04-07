from random import sample
import os

def parse(civlist: str) -> set:
    return set(map(str.strip, civlist.strip().split(";")))

#source: https://stackoverflow.com/questions/579687/how-do-i-copy-a-string-to-the-clipboard
def addToClipBoard(text):
    command = 'echo ' + text.strip() + ' | clip'
    os.system(command)

civs = """
    Morocco; Greece; Assyria; Songhai; The Huns; Rome;
    Germany; The Celts; Poland; Russia; Persia; Carthage;
    England; Venice; Indonesia; India; Mongolia; Sweden;
    Ethiopia; Denmark; Arabia; Iroquois; Spain; Polynesia;
    Portugal; Austria; Aztec; France; Babylon; Japan; The Maya;
    The Inca; Brazil; Shoshone; Egypt; Siam; Korea; The Zulu;
    The Ottomans; Byzantium; America; The Netherlands; China
"""

remove = """
    Venice, Korea, Brazil
"""

if __name__ == "__main__":
    population = list(parse(civs) - parse(remove))
    players = input("List the players separated by space: ").split(" ")
    
    choices = sample(population, k=len(players))
    
    res = "\""
    for p, c in zip(players, choices):
        res += p + ": ||" + c + "||" + "    "
    res += "\""
    addToClipBoard(res)