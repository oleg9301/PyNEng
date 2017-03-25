# -*- coding: utf-8 -*-

'''
Задание 9.1

Создать скрипт, который будет ожидать два аргумента:
    1. имя файла, в котором находится вывод команды show
    2. регулярное выражение

В результате выполнения скрипта, на стандартный поток вывода должны быть
выведены те строки из файла с выводом команды show,
в которых было найдено совпадение с регулярным выражением.

Проверить работу скрипта на примере вывода команды sh ip int br
(файл sh_ip_int_br.txt).
Например, попробуйте вывести информацию только по интерфейсу FastEthernet0/1.
'''

from sys import argv
from re import search

try:
    file_name = argv[1]
    regex = argv[2]
    with open(file_name, 'r') as f:
        file_string = f.read().strip().split('\n')
        for string in file_string:
            if search(regex, string):
                print(string)
except IndexError:
    print('Please give two arguments for app {}'.format(argv[0]))
except OSError:
    print('File {} not found'.format(file_name))
