# -*- coding: utf-8 -*-

'''
Это копия скрипта get_data_ver1.py из раздела
'''

import sqlite3
import sys

db_filename = 'dhcp_snooping.db'
fileds_table = ['mac', 'ip', 'vlan', 'interface', 'switch']


def two_arg():
    key, value = sys.argv[1:]
    keys = ['mac', 'ip', 'vlan', 'interface']
    keys.remove(key)
    with sqlite3.connect(db_filename) as conn:
        conn.row_factory = sqlite3.Row
        print("\nDetailed information for host(s) with", key, value)
        print('-' * 40)
        query = "select * from dhcp where {} = ?".format(key)
        result = conn.execute(query, (value,))
        for row in result:
            for k in keys:
                print("{:12}: {}".format(k, row[k]))
            print('-' * 40)


def no_arg():
    with sqlite3.connect(db_filename) as conn:
        print('В таблице dhcp такие записи:', '\n' + '-' * 40)
        query = "select * from dhcp"
        result = conn.execute(query)
        for column in result:
            print("%-20s %-18s %-5s %-18s %-2s" % column)


if len(sys.argv) == 3:
    if sys.argv[1] in fileds_table:
        two_arg()
    else:
        print('Данный параметр не поддерживается.\n'
              'Допустимые значения параметров:', ', '.join(fileds_table))
elif len(sys.argv) == 1:
    no_arg()
else:
    sys.exit('Пожалуйста, введите два или ноль аргументов')
