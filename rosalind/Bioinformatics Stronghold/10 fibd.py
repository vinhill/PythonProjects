#simulate rabbit reproduction take 2
#amount of rabbits after n months with lifespan of m months  
n, m = int(input("n: ")), int(input("m: "))

prev = list()

for i in range(n+1):
  if i <= 0 or m <= 0:
    prev.append(0)
  elif i == 1 or i == 2:
    prev.append(1)
  elif i-m-1 < 0:
    prev.append( prev[i-1] + prev[i-2] )
  elif i == m+1:
     prev.append( prev[i-1] + prev[i-2] - prev[i-m-1] - 1 )
  else:
    try:
      prev.append( prev[i-1] + prev[i-2] - prev[i-m-1] )
    except IndexError:
      print("Indexerror at {}".format(i))

print(prev[n])