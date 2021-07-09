#find all positions where substring appears in string
str = input("Please enter DNA sequence: ")
sub = input("Please enter DNA subsequence: ")
i = -1
while(True):
  try:
    i = str.index(sub, i+1)
    print("{0} ".format(i+1), end="")
  except ValueError:
    break