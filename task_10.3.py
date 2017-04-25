# -*- coding: utf-8 -*-

'''
Задание 10.3

Создать функцию parse_sh_cdp_neighbors, которая обрабатывает
вывод команды show cdp neighbors.

Функция ожидает, как аргумент, вывод команды одной строкой.

Функция должна возвращать словарь, который описывает соединения между устройствами.

Например, если как аргумент был передан такой вывод:
R4>show cdp neighbors

Device ID    Local Intrfce   Holdtme     Capability       Platform    Port ID
R5           Fa 0/1          122           R S I           2811       Fa 0/1
R6           Fa 0/2          143           R S I           2811       Fa 0/0

Функция должна вернуть такой словарь:

{'R4': {'Fa0/1': {'R5': 'Fa0/1'},
        'Fa0/2': {'R6': 'Fa0/0'}}}


Проверить работу функции на содержимом файла sh_cdp_n_sw1.txt
'''


def parse_sh_cdp_neighbors(file_str):
    i = False
    cdp_dict = {}
    for j in file_str:
        if 'neighbors' in j.split():
            i = False
            localhost_name = j.split()[0][:-5]
        elif 'Device' in j.split():
            i = True
        elif i:
            key_cdp = (localhost_name, j.split()[1] + j.split()[2])
            value_cdp = (j.split()[0], j.split()[-2] + j.split()[-1])
            if value_cdp not in cdp_dict.keys():
                cdp_dict[key_cdp] = value_cdp
    return cdp_dict


with open('sh_cdp_n_sw1.txt', 'r') as f:
    print(parse_sh_cdp_neighbors(f.read().strip().split('\n')))
