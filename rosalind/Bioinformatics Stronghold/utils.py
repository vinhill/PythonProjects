
class FASTAReader:
  
    #string input gives an alternative input source
    def __init__(self, filepath, string_input=None):
        self.path = filepath
        if filepath:
            self.file = open(self.path, 'r')
        else:
            self.file = None
        
        if string_input:
            self.str_lines = string_input.split("\n")
        else:
            self.str_lines = None
        
        self.eof = False
        self.str_line = -1
        
        self.cur_id = self.__nextLine()[1:-1]
    
    def __nextLine(self):
        if self.file:
            return self.file.readline()
        else:
            self.str_line += 1
            if self.str_line >= len(self.str_lines):
                return ""
            else:
                return self.str_lines[self.str_line] + "\n"

    def __iter__(self):
        return self

    def reset(self):
        if self.file:
            self.file.close()
            self.file = open(self.path, 'r')
        
        self.eof = False
        self.str_line = -1
        
        self.cur_id = self.__nextLine()[1:-1]

    def next(self):
        if self.eof:
            if self.file:
                self.file.close()
            raise StopIteration
        dna = ""
        line = self.__nextLine()
        while line != "" and not line.startswith('>'):
            dna += line
            line = self.__nextLine()
        id = self.cur_id
        if line != "":
            self.cur_id = line[1:-1]
        else:
            self.eof = True
        return (id, dna.replace("\n", ""))

    def nextDNA(self):
        id, dna = self.next()
        return dna

    def __next__(self):
        return self.next()

    def remainingList(self):
        res = list()
        for id, dna in self:
            res.append((id,dna))
        return res

    def remainingDNAList(self):
        res = list()
        for id, dna in self:
            res.append(dna)
        return res


class BioInfUtils:

    def getUniprotFASTA(uniprot_id):
        from urllib.request import urlopen
                
        content = urlopen(
            "http://www.uniprot.org/uniprot/{0}.fasta".format(uniprot_id)
            ).read().decode('utf-8')
        id = content[1:content.find("\n")]
        dna = content[content.find("\n"):].replace("\n","")
        
        return {"id": id, "dna": dna}

    def getCodonDict():
        file = open("codon table.txt")
        codon_dict = dict()
        for line in file:
          entries = line.split("      ")
          for e in entries:
            codon_dict[e[0:3]] = e[4:5]
        file.close()
        return codon_dict
  
    def reverseComplement(dna):
        rc = list()
        for c in dna[::-1]:
            if c == 'A':
              rc.append('T')
            elif c == 'T':
              rc.append('A')
            elif c == 'C':
              rc.append('G')
            elif c == 'G':
              rc.append('C')
        return "".join(rc)
    
    def rnaToAAS(rna):
        codon_dict = BioInfUtils.getCodonDict()
        aas = list()
        for i in range(0,len(rna),3):
            aas.append( codon_dict[ rna[i:i+3] ] )
        return "".join(aas)


class Utils:
    
    def bin_search(list, val):
        l = 0
        r = len(list)-1
        while l <= r:
            m = int((l+r)/2)
            if list[m] == val:
                return (m,m)
            elif list[m] > val:
                r = m-1
            else:
                l = m+1
        return (r,l)
    
    # first element for which comp(list element, val) is true
    def lower_bound(list, val, comp):
        l = 0
        r = len(list)
        while l < r:
            m = (l+r)//2
            if comp(list[m], val):
                r = m
            else:
                l = m+1
        return l

    def binom_coeff(n, k):
        from functools import reduce
        from operator import mul
        if k > n or k < 0 or n < 0:
            return 0
        elif n == k:
            return 1
        elif k > n-k:
            return int(reduce(mul, range(k+1,n+1),1) / reduce(mul, range(1,n-k+1),1))
        else:
            return int(reduce(mul, range(n-k+1,n+1),1) / reduce(mul, range(1,k+1),1))
        
    def binom_dist(n,k,p):#P(X=k) also k treffer aus n versuchen mit prob. p
        return Utils.binom_coeff(n,k) * p**k * (1-p)**(n-k)

    def binom_cdf(n,k,p):#P(X<=k)
        return sum(Utils.binom_dist(n,i,p) for i in range(0,k+1))
        
    def fak(n):
        import math
        return math.factorial(n)
    

class Trie:
    def __init__(self):
        self.children = {}
        self.value = None

    def set(self, value):
        self.value = value

    def get(self):
        return self.value

    def append(self, label):
        self.children[label] = Trie()
        return self.children[label]
    
    def has(self, label):
        return label in self.children
    
    def _add(self, path, i):
        if len(path) == i:
            return self
        elif self.has(path[i]):
            return self.children[path[i]]._add(path, i+1)
        else:
            return self.append(path[i])._add(path, i+1)
    
    def add(self, path, value):
        n = self._add(path, 0)
        n.set(value)

    def _walk(self, path, i):
        if len(path) == i:
            return self
        elif not self.has(path[i]):
            return None
        else:
            return self.children[path[i]]._walk(path, i+1)
        
    def walk(self, path):
        return self._walk(path, 0)
