n = int(input())

doc = {}

for _ in range(n):
    command = input().split()

    if command[0] == "set":
        key = command[1]
        value = command[2]
        doc[key] = value

    elif command[0] == "get":
        key = command[1]
        if key in doc:
            print(doc[key])
        else:
            print(f"KE: no key {key} found in the document")






















# n — количество команд

# {} — это пустой словарь
# doc — наша «база данных» (документ MongoDB)
# doc = {}     словарь = документ MongoDB
# Он будет хранить: ключ → значение
# Ex: "some_key" → "some_value"


# range(n) — создаёт последовательность от 0 до n-1
# цикл выполнится ровно n раз

# _ — имя переменной, которое означает:
# «значение мне не важно, просто повтори n раз»


# command — список слов команды
# command = input().split()
# input() читает одну строку команды, например: get some_key
# .split() разбивает строку по пробелам, превращает её в список слов. Ex: "get some_key".split()  → ["get", "some_key"]

# if command[0] == "set" Explanation:
# command[0] — первое слово команды
# если это "set" → значит команда добавить / изменить значение

# key = command[1]
# value = command[2]
# command[1] — ключ
# command[2] — значение


# doc[key] = value
# если ключа не было → он добавится
# если ключ уже был → значение перезапишется
# Это поведение словаря по умолчанию, не нужно ничего дополнительно проверять.
# Это и есть команда set.

# elif command[0] == "get"
# если команда не set, проверяем — get
# get означает: попробовать получить значение по ключу

# key = command[1]
# берём ключ, по которому нужно искать значение
# Ex: ["get", "name"] → key = "name"

# if key in doc:
# проверка: есть ли такой ключ в словаре
# in возвращает True или False

# print(doc[key])
# если ключ найден → выводим связанное с ним значение
# doc[key] — это значение, которое хранится по этому ключу

# else:
#    print(f"KE: no key {key} found in the document")
# если ключа нет: печатаем сообщение об ошибке в точном формате
# f"..." — f-строка, позволяет вставить значение key прямо в текст












"""
Из-за того, что код на сайте не проходил все 100 тестов, а лишь 83, я сделала новый более бысьрый код, с более быстрым вводом и выводом.

import sys

input = sys.stdin.readline

n = int(input())
doc = {}
out = []

for _ in range(n):
    parts = input().split()

    if parts[0] == "set":
        key = parts[1]
        value = parts[2]
        doc[key] = value

    else:  # get
        key = parts[1]
        if key in doc:
            out.append(doc[key])
        else:
            out.append(f"KE: no key {key} found in the document")

sys.stdout.write("\n".join(out))

"""





























"""
Нужно эмулировать один документ MongoDB.

Документ — это просто хранилище вида:

ключ → значение


Правила:

Ключи уникальны

Команда set key value

если ключа не было → добавить

если ключ уже был → заменить значение

Команда get key

если ключ есть → вывести значение

если ключа нет → вывести сообщение об ошибке в точном формате


Решение:

Мы используем словарь (dict), потому что:

он идеально подходит для key → value

проверка наличия ключа быстрая

замена значения делается автоматически
"""




