# -*- coding: utf-8 -*-
'''
Задание 14.2

В этом задании нужно использовать функцию parse_output из задания 14.1.
Она используется для того, чтобы получить структурированный вывод
в результате обработки вывода команды.

Полученный вывод нужно записать в CSV формате.

Для записи вывода в CSV, нужно создать функцию list_to_csv, которая ожидает как аргументы:
* список:
 * первый элемент - это список с названиями заголовков
 * остальные элементы это списки, в котором находятся результаты обработки вывода
* имя файла, в который нужно записать данные в CSV формате

Проверить работу функции на примере обработки команды sh ip int br (шаблон и вывод есть в разделе).
'''


import sys
import csv
import textfsm

template = sys.argv[1]
output_file = sys.argv[2]


def parse_output(template, output):
    with open(template) as template, open(output_file) as output:
        re_table = textfsm.TextFSM(template)
        header = re_table.header
        result = re_table.ParseText(output.read())
    return [header] + result


def list_to_csv(list, file):
    with open(file, 'w') as f:
        map(csv.writer(f).writerow, list)

list_to_csv((parse_output(template, output_file)), 'text.csv')
