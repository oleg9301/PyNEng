# -*- coding: utf-8 -*-

'''
Задание 9.4

Создать функцию parse_show, которая ожидает два аргумента:
* имя файла, в котором находится вывод команды show
* регулярное выражение

Функция должна обрабатывать вывод команды show ip int br и возвращать такие поля:
* Interface
* IP-Address
* Status
* Protocol

Информация должна возвращаться в виде списка кортежей:
[('FastEthernet0/0', '10.0.1.1', 'up', 'up'),
 ('FastEthernet0/1', '10.0.2.1', 'up', 'up'),
 ('FastEthernet0/2', 'unassigned', 'up', 'up')]

Для получения такого результата, используйте регулярные выражения.

Проверить работу функции на примере файла sh_ip_int_br_2.txt.
'''
from re import findall, compile


def parse_show(file_name, regex):
    result = []
    try:
        with open(file_name, 'r') as f:
            file_string = f.read().strip().split('\n')
            for string in file_string:
                result.extend(findall(regex, string))
    except OSError:
        print('File {} not found'.format(file_name))
    return result

regex = compile('(Fast\w*/\d|Loo\w*)\s*(\d+\.\d+\.\d+\.\d+|una\w*)\s*(\w*)\s*(\w*)\s*(up|adm\w*\s\w*)\s*(\w*)')
print(parse_show('sh_ip_int_br_2.txt', regex))
