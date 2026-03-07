class StringHandler:
    def __init__(self):
        self.s = ""

    def getString(self):
        self.s = input()

    def printString(self):
        print(self.s.upper())

handler = StringHandler()
handler.getString()
handler.printString()
































# Создаем класс. Класс — это шаблон, по которому мы будем создавать объекты.
# Название 'StringHandler' менять можно, но лучше оставить как в условии.
class StringHandler:
    
    # Метод __init__ выполняется автоматически при создании объекта.
    # Здесь мы создаем "переменную внутри класса" (атрибут), чтобы хранить текст.
    def __init__(self):
        # self.s — это наше хранилище. Название 's' можно поменять на любое другое.
        self.s = ""

    # Метод для ввода строки.
    def getString(self):
        # input() считывает то, что ты ввел в консоль.
        # Результат записывается в self.s, чтобы другие методы могли его видеть.
        self.s = input()

    # Метод для вывода строки.
    def printString(self):
        # self.s.upper() — берет нашу строку и делает все буквы заглавными.
        # print() выводит результат на экран.
        print(self.s.upper())

# Создаем экземпляр (объект) класса. 
# Название переменной 'handler' можно менять на любое свое.
handler = StringHandler()

# Вызываем метод получения строки. Программа будет ждать, пока ты что-то введешь.
handler.getString()

# Вызываем метод печати. Программа возьмет твой ввод и выведет его капсом.
handler.printString()