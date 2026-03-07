class Pair:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def add(self, other_pair):
        sum_a = self.a + other_pair.a
        sum_b = self.b + other_pair.b
        return sum_a, sum_b

data = input().split()
a1, b1 = int(data[0]), int(data[1])
a2, b2 = int(data[2]), int(data[3])

pair1 = Pair(a1, b1)
pair2 = Pair(a2, b2)

res_a, res_b = pair1.add(pair2)
print(f"Result: {res_a} {res_b}")



















# Создаем класс Pair (тема L3.5). 
# Он будет хранить два числа как одно целое.
class Pair:
    
    # Конструктор принимает два числа и сохраняет их в атрибуты (L3.5).
    def __init__(self, a, b):
        self.a = a
        self.b = b

    # Метод add принимает другой объект этого же класса (other_pair).
    def add(self, other_pair):
        # Мы складываем 'a' текущего объекта (self.a) 
        # с 'a' другого объекта (other_pair.a).
        sum_a = self.a + other_pair.a
        
        # То же самое делаем для 'b'.
        sum_b = self.b + other_pair.b
        
        # Возвращаем два значения сразу (L3.1). 
        # В Python это вернется как кортеж (Tuple L2.4).
        return sum_a, sum_b

# Считываем ввод. Мы получаем строку, например "1 2 3 4".
# .split() разбивает её на список строк: ["1", "2", "3", "4"] (L1.8).
data = input().split()

# Превращаем строки в целые числа и распределяем по переменным (L1.7).
a1, b1 = int(data[0]), int(data[1])
a2, b2 = int(data[2]), int(data[3])

# Создаем два отдельных объекта (экземпляра) нашего класса.
pair1 = Pair(a1, b1)
pair2 = Pair(a2, b2)

# Вызываем метод add у первого объекта и передаем ему второй объект.
# Результат (два числа) сохраняем в переменные res_a и res_b.
res_a, res_b = pair1.add(pair2)

# Выводим результат в формате, который требует условие.
# Используем f-строку для вставки переменных в текст (L1.9).
print(f"Result: {res_a} {res_b}")