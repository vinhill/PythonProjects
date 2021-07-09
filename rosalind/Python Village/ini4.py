a, b = (4092, 8115)

sum = 0
a = a if a % 2 == 1 else a+1

for i in range(a, b+1, 2):
  sum += i
  
print(sum)