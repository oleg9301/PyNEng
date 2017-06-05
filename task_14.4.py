# -*- coding: utf-8 -*-
'''
Задание 14.4

На основе примера из раздела [clitable](https://natenka.gitbooks.io/pyneng/content/book/14_textfsm/3_textfsm_clitable.html) сделать функцию parse_command_dynamic.

Параметры функции:
* словарь атрибутов, в котором находятся такие пары ключ: значение:
 * 'Command': команда
 * 'Vendor': вендор (обратите внимание, что файл index отличается от примера, который использовался в разделе, поэтому вам нужно подставить тут правильное значение)
* имя файла, где хранится соответствие между командами и шаблонами (строка)
 * значение по умолчанию аргумента - index
* каталог, где хранятся шаблоны и файл с соответствиями (строка)
 * значение по умолчанию аргумента - templates
* вывод команды (строка)

Функция должна возвращать список словарей с результатами обработки вывода команды (как в задании 14.1a):
* ключи - названия столбцов
* значения - соответствующие значения в столбцах

Проверить работу функции на примере вывода команды sh ip int br.

Пример из раздела:
'''

import textfsm.clitable as clitable

attributes = {'Command': 'show ip route ospf', 'Vendor': 'cisco_ios'}


def parse_command_dynamic(attributes, output, index='index', templates='templates'):
    with open(output, 'r') as output:
        cli_table = clitable.CliTable(index, templates)
        cli_table.ParseCmd(output.read(), attributes)

        data_rows = []

        for row in cli_table:
            current_row = []
            for value in row:
                current_row.append(value)
            data_rows.append(current_row)

        header = []
        for name in cli_table.header:
            header.append(name)

        output_list = []
        for row in data_rows:
            output_list.append(dict(zip(header, row)))
    return output_list

print(parse_command_dynamic(attributes, 'output/sh_ip_route_ospf.txt'))
