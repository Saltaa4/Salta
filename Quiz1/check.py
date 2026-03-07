num = list(map(int , input().split())) 

avg = sum(num)/ len(num) 
count =0 

for i in range (1 , len(num)): 
    if i < avg: 
     count += 1 

print (count )