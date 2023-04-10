# Задание 1

VAR_1 = 'разработка'
VAR_2 = 'сокет'
VAR_3 = 'декоратор'

STR_LIST = [VAR_1, VAR_2, VAR_3]

for el in STR_LIST:
    print(type(el))
    print(el)

print()


VAR_UNIC_1 = '\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430'
VAR_UNIC_2 = '\u0441\u043e\u043a\u0435\u0442'
VAR_UNIC_3 = '\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440'

UNIC_LIST = [VAR_UNIC_1, VAR_UNIC_2, VAR_UNIC_3]

for el in UNIC_LIST:
    print(type(el))
    print(el)

# Задание 2

STR_A = b'class'
STR_B = b'function'
STR_C = b'method'

STR_LIST = [STR_A, STR_B, STR_C]

for el in STR_LIST:
    print(type(el))
    print(el)
    print(len(el))


print(type(type(3)))

# Задание 3

VAR_1 = 'attribute'
VAR_2 = 'класс'
VAR_3 = 'функция'
VAR_4 = 'type'

VAR_LIST = [VAR_1, VAR_2, VAR_3, VAR_4]

for el in VAR_LIST:
    try:
        print('Слово записано в байтовом типе:', eval(f'b"{el}"'))
    except SyntaxError:
        print(
            f'Слово "{el}" невозможно записать в байтовом типе с помощью префикса b')

# Задание 4

VAR_1_STR = 'разработка'
VAR_2_STR = 'администрирование'
VAR_3_STR = 'protocol'
VAR_4_STR = 'standard'

STR_LIST = [VAR_1_STR, VAR_2_STR, VAR_3_STR, VAR_4_STR]

ELEMS_B = []
for el in STR_LIST:
    el_b = el.encode('utf-8')
    ELEMS_B.append(el_b)

print(ELEMS_B)
print()

ELEMS_STR = []
for el in ELEMS_B:
    el_str = el.decode('utf-8')
    ELEMS_STR.append(el_str)

print(ELEMS_STR)

# Задание 5

import subprocess
import chardet

ARGS = ['ping', 'yandex.ru']
YA_PING = subprocess.Popen(ARGS, stdout=subprocess.PIPE)
for line in YA_PING.stdout:
    result = chardet.detect(line)
    print(result)
    line = line.decode(result['encoding']).encode('utf-8')
    print(line.decode('utf-8'))

# Задание 6

from chardet import detect

with open('test.txt', encoding='utf-8') as file:
    for line in file.read():
        print(line)

file = open('test.txt', 'rb')
for line in file:
    print(line.decode(encoding='utf-8'))
file.close()
