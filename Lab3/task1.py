n = input()

for digit in n:
    if int(digit) % 2 != 0:  
        print("Not valid")
        break
else:
    print("Valid")
