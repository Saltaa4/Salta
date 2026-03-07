num = list(map(int , input().split())) 

avg = sum(num)/ len(num) 
count =0 

for i in range (1 , len(num)): 
    if i < avg: 
     count += 1 

print (count )



# Count how many numbers in the array are greater than its average value.



# Chat GPT:

nums = list(map(int, input().split()))

avg = sum(nums) / len(nums)

count = 0
for i in nums:
    if i > avg:
        count += 1

print(count)
