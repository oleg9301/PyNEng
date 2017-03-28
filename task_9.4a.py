# -*- coding: utf-8 -*-

'''
Задание 9.4a

Создать функцию convert_to_dict, которая ожидает два аргумента:
* список с названиями полей
* список кортежей с результатами отработки функции parse_show из задания 9.4

Функция возвращает результат в виде списка словарей (порядок полей может быть другой):
[{'interface': 'FastEthernet0/0', 'status': 'up', 'protocol': 'up', 'address': '10.0.1.1'},
 {'interface': 'FastEthernet0/1', 'status': 'up', 'protocol': 'up', 'address': '10.0.2.1'}]

Проверить работу функции на примере файла sh_ip_int_br_2.txt:
* первый аргумент - список headers
* второй аргумент - результат, который возвращает функции parse_show из прошлого задания.

Функцию parse_show не нужно копировать.
Надо импортировать или саму функцию, и использовать то же регулярное выражение,
что и в задании 9.4, или импортировать результат выполнения функции parse_show.

'''

from re import compile
from task_9_4 import parse_show

regex = compile('(Fast\w*/\d|Loo\w*)\s*(\d+\.\d+\.\d+\.\d+|una\w*)\s*\w*\s*\w*\s*(up|adm\w*\s\w*)\s*(\w*)')
file_name = 'sh_ip_int_br_2.txt'
headers = ['interface', 'address', 'status', 'protocol']
parse_show_result = parse_show(file_name, regex)


def convert_to_dict(headers, parse_show_result):
    result = []
    for string in parse_show_result:
        result.append(dict(zip(headers, string)))
    return result

print(convert_to_dict(headers, parse_show_result))
