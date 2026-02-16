num_to_str = {
    '0': "ZER", '1': "ONE", '2': "TWO", '3': "THR", '4': "FOU", 
    '5': "FIV", '6': "SIX", '7': "SEV", '8': "EIG", '9': "NIN"
}

str_to_num = {
    "ONE": "1", "TWO": "2", "THR": "3", "FOU": "4", "FIV": "5",
    "SIX": "6", "SEV": "7", "EIG": "8", "NIN": "9", "ZER": "0"
}

def string_to_int(s):
    res_digits = ""
    for i in range(0, len(s), 3):
        triplet = s[i:i+3]
        res_digits += str_to_num[triplet]
    return int(res_digits)

def int_to_string(n):
    res_words = ""
    n_str = str(n)
    for digit in n_str:
        res_words += num_to_str[digit]
    return res_words

def string_calculator(expression):
    if '+' in expression:
        op = '+'
    elif '-' in expression:
        op = '-'
    else:
        op = '*'
    
    parts = expression.split(op)
    val1 = string_to_int(parts[0])
    val2 = string_to_int(parts[1])
    
    if op == '+':
        result = val1 + val2
    elif op == '-':
        result = val1 - val2
    else:
        result = val1 * val2
    
    return int_to_string(result)

expression = input().strip()
print(string_calculator(expression))
