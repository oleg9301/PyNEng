# -*- coding: utf-8 -*-

'''
Задание 9.3

Создать функцию parse_cfg, которая ожидает как аргумент имя файла, в котором находится конфигурация устройства.

Функция должна обрабатывать конфигурацию и возвращать IP-адреса и маски,
которые настроены на интерфейсах, в виде списка кортежей:
* первый элемент кортежа - IP-адрес
* второй элемент кортежа - маска

Например (взяты произвольные адреса):
[('10.0.1.1', '255.255.255.0'), ('10.0.2.1', '255.255.255.0')]

Для получения такого результата, используйте регулярные выражения.

Проверить работу функции на примере файла config_r1.txt.

Обратите внимание, что в данном случае, мы можем не проверять корректность IP-адреса,
диапазоны адресов и так далее, так как мы обрабатываем конфигурацию, а не ввод пользователя.
'''

from re import findall


def parse_cfg(file_name):
    result = []
    regex = '(\d+\.\d+\.\d+\.\d+)'
    try:
        with open(file_name, 'r') as f:
            file_string = f.read().strip().split('\n')
            for string in file_string:
                regex_match = findall(regex, string)
                if regex_match and 'address' in string:
                    result.append(tuple(x for x in regex_match))
    except OSError:
        print('File {} not found'.format(file_name))
    return result

print(parse_cfg('config_r1.txt'))
