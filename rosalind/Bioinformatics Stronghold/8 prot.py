#compute primary sequence of a protein form rna sequence
rna = input("Please input rna sequence: ")

#generate codon dict
file = open("codon table.txt")
codon_dict = dict()
for line in file:
  entries = line.split("      ")
  for e in entries:
    codon_dict[e[0:3]] = e[4:5]
file.close()

#generate AS sequence
ass = list()
for i in range(0,len(rna),3):
  ass.append( codon_dict[ rna[i:i+3] ] )
print("".join(ass))