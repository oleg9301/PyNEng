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


def parse_sh_cdp_neighbors(cdp_file):
    i = False
    local_interfaces, result = {}, {}
    for cdp_string in cdp_file:
        if 'neighbors' in cdp_string.split():
            i = False
            localhost_name = cdp_string.split()[0][:-5]
        elif 'Device' in cdp_string.split():
            i = True
        elif i:
            remote_host, local_interface = {}, {}
            remote_host[cdp_string.split()[0]] = cdp_string.split()[-2] + cdp_string.split()[-1]
            local_interface[(cdp_string.split()[1] + cdp_string.split()[2])] = remote_host
            local_interfaces.update(local_interface)
    result[localhost_name] = local_interfaces
    return result


if __name__ == '__main__':
    with open('sh_cdp_n_sw1.txt', 'r') as f:
        print(parse_sh_cdp_neighbors(f.read().strip().split('\n')))
