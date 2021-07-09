str = input("Please enter input: ")

nums = list(map(lambda x: int(x), str.split(" ")))
probs = [1,1,1,0.75,0.5,0]

res = 0
for i in range(len(nums)):
  res += nums[i] * probs[i] * 2

print(res)