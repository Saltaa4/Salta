num_to_str = {
    '0': "ZER", '1': "ONE", '2': "TWO", '3': "THR", '4': "FOU", 
    '5': "FIV", '6': "SIX", '7': "SEV", '8': "EIG", '9': "NIN"
}

str_to_num = {v: k for k, v in num_to_str.items()}

def string_to_int(s):
    digits = [str_to_num[s[i:i+3]] for i in range(0, len(s), 3)]
    return int("".join(digits))

def int_to_string(n):
    return "".join([num_to_str[d] for d in str(n)])

def string_calculator(expression):
    for op in ['+', '-', '*']:
        if op in expression:
            parts = expression.split(op)
            val1 = string_to_int(parts[0])
            val2 = string_to_int(parts[1])
            
            if op == '+': result = val1 + val2
            elif op == '-': result = val1 - val2
            elif op == '*': result = val1 * val2
            
            return int_to_string(result)

expression = input().strip()
print(string_calculator(expression))




































# Словарь, где цифра (ключ) связана с её строковым названием (значение).
# Названия "ZER", "ONE" и т.д. менять нельзя — их требует проверяющая система.
# А вот название самого словаря 'num_to_str' можно изменить на любое другое.
num_to_str = {
    '0': "ZER", '1': "ONE", '2': "TWO", '3': "THR", '4': "FOU", 
    '5': "FIV", '6': "SIX", '7': "SEV", '8': "EIG", '9': "NIN"
}

# Мы создаем "обратный" словарь: берем значения из первого и делаем их ключами.
# Получится: {"ONE": "1", "TWO": "2", ...}. Это нужно для перевода слов в цифры.
str_to_num = {v: k for k, v in num_to_str.items()}

# Функция для превращения строки "ONETWO" в число 12.
def string_to_int(s):
    # s[i:i+3] — берем кусочек строки по 3 символа (триплеты).
    # Превращаем каждый триплет в цифру через наш словарь str_to_num.
    digits = [str_to_num[s[i:i+3]] for i in range(0, len(s), 3)]
    # Склеиваем цифры ["1", "2"] в строку "12" и превращаем в целое число int.
    return int("".join(digits))

# Функция для превращения числа 48 обратно в "FOUEIG".
def int_to_string(n):
    # Превращаем число в строку '48', берем каждую цифру '4' и '8',
    # находим для них "имена" в словаре num_to_str и склеиваем их.
    return "".join([num_to_str[d] for d in str(n)])

# Главная функция-калькулятор.
def string_calculator(expression):
    # Проверяем, какой знак операции в строке.
    for op in ['+', '-', '*']:
        if op in expression:
            # Разрезаем строку на две части по знаку операции.
            parts = expression.split(op)
            
            # Переводим левую и правую части из слов в обычные числа.
            val1 = string_to_int(parts[0])
            val2 = string_to_int(parts[1])
            
            # Выполняем само математическое действие.
            if op == '+': result = val1 + val2
            elif op == '-': result = val1 - val2
            elif op == '*': result = val1 * val2
            
            # Превращаем результат обратно в слова и возвращаем.
            return int_to_string(result)

# Считываем входную строку и убираем лишние пробелы по краям (.strip()).
expression = input().strip()

# Вызываем функцию и выводим итоговый результат.
print(string_calculator(expression))