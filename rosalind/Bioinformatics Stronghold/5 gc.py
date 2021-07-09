#compute gc-content
def gc_content(dna):
  gc = 0
  for c in dna:
    if c == 'C' or c == 'G':
      gc += 1
  return round(gc / len(dna), 6)

#print gc content for all dna strings in file
file = open("5 gc.txt")
dna = ""
id = ""
for line in file:
  if line.startswith('>'):
    if dna != "":
      print("FASTA {0} has GC-content {1}".format(id, gc_content(dna)))
    dna=""
    id=line[1:-1]
  else:
    dna = dna + line[:-1]
if dna != "":
print("FASTA {0} has GC-content {1}".format(id, gc_content(dna)))