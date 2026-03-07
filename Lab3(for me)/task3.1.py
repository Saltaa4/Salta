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

































# Словари для перевода (L2.6 Dictionaries)
num_to_str = {
    '0': "ZER", '1': "ONE", '2': "TWO", '3': "THR", '4': "FOU", 
    '5': "FIV", '6': "SIX", '7': "SEV", '8': "EIG", '9': "NIN"
}

str_to_num = {
    "ONE": "1", "TWO": "2", "THR": "3", "FOU": "4", "FIV": "5",
    "SIX": "6", "SEV": "7", "EIG": "8", "NIN": "9", "ZER": "0"
}

# Функция превращает "ONETWO" в 12 (L3.1 Functions)
def string_to_int(s):
    res_digits = ""
    # Идем по строке с шагом 3 (L2.3 Slicing)
    for i in range(0, len(s), 3):
        triplet = s[i:i+3] # Берем по 3 буквы
        res_digits += str_to_num[triplet] # Находим цифру и приклеиваем к строке
    return int(res_digits) # В конце превращаем "12" в число 12 (L1.7 Type casting)

# Функция превращает 48 в "FOUEIG"
def int_to_string(n):
    res_words = ""
    n_str = str(n) # Превращаем число в строку "48", чтобы по нему можно было идти циклом
    # Перебираем каждую цифру (L2.2 For loops)
    for digit in n_str:
        res_words += num_to_str[digit] # Добавляем слово (например, "FOU") к результату
    return res_words

# Основная логика
def string_calculator(expression):
    # Определяем оператор (L1.12 Conditions)
    if '+' in expression:
        op = '+'
    elif '-' in expression:
        op = '-'
    else:
        op = '*'
    
    # Разбиваем строку по знаку (L1.8 Strings methods)
    parts = expression.split(op)
    val1 = string_to_int(parts[0])
    val2 = string_to_int(parts[1])
    
    # Считаем результат (L1.11 Operators)
    if op == '+':
        result = val1 + val2
    elif op == '-':
        result = val1 - val2
    else:
        result = val1 * val2
    
    # Переводим число обратно в "слова"
    return int_to_string(result)

# Точка входа в программу
expression = input().strip()
print(string_calculator(expression))