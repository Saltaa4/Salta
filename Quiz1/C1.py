a, b = map(int, input().split())

result = a**2 + 2*a*b + b**2

print(result)




# You are given two integers a and b.
# Compute the value of the expression:
# (a + b)²
# Use the algebraic identity for the square of a sum.
# Print the result.

# If we just use algebraic identity, solution would be: print((a + b) ** 2)

# or another option: 
nums = list(map(int, input().split()))

a = nums[0]
b = nums[1]

result = a**2 + 2*a*b + b**2

print(result)
