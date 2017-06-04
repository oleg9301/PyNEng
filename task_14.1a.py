# -*- coding: utf-8 -*-
'''
Задание 14.1a

Переделать функцию parse_output из задания 14.1 таким образом,
чтобы, вместо списка списков, она возвращала один список словарей:
* ключи - названия столбцов,
* значения, соответствующие значения в столбцах.

То есть, для каждой строки будет один словарь в списке.
'''

import sys
import textfsm

template = sys.argv[1]
output_file = sys.argv[2]


def parse_output(template, output):
    output_list = []
    with open(template) as template, open(output_file) as output:
        re_table = textfsm.TextFSM(template)
        header = re_table.header
        result = re_table.ParseText(output.read())
        for string in result:
            output_list.append(dict(zip(header, string)))
    return output_list

print(parse_output(template, output_file))

