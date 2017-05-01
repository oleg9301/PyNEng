# -*- coding: utf-8 -*-

"""
Задание 11.5a

После выполнения задания 11.5, в таблице dhcp есть новое поле last_active.

Обновите скрипт add_data.py, таким образом, чтобы он удалял все записи,
которые были активными более 7 дней назад.

Для того, чтобы получить такие записи, можно просто вручную обновить поле last_active.

В файле задания описан пример работы с объектами модуля datetime.
Обратите внимание, что объекты, как и строки с датой, которые пишутся в БД,
можно сравнивать между собой.

"""

import sqlite3
import re
import glob
import yaml
import os
import sys
from datetime import datetime, timedelta


db_filename = 'dhcp_snooping.db'
schema_filename = 'dhcp_snooping_schema.sql'
dhcp_snoop_files = glob.glob('sw*_dhcp_snooping.txt')
regex = re.compile('(.+?) +(.*?) +\d+ +[\w-]+ +(\d+) +(.*$)')
db_exists = os.path.exists(db_filename)
now = str(datetime.today().replace(microsecond=0))
week_ago = str(datetime.today().replace(microsecond=0) - timedelta(days=7))


def check_db(func):
    def check_info():
        if not db_exists:
            sys.exit('Database does not exists. Please create dhcp_snooping.db')
        func()
    return check_info


@check_db
def add_into_dhcp():
    with sqlite3.connect(db_filename) as conn:
        conn.execute('update  dhcp set active = 0')
        current_mac_table = conn.execute('select mac from dhcp').fetchall()
        last_active_table = conn.execute('select last_active from dhcp').fetchall()
        for data_filename in dhcp_snoop_files:
            with open(data_filename) as data:
                result = [regex.search(line).groups() for line in data if line[0].isdigit()]
            for string in result:
                if (string[0], ) in current_mac_table:
                    conn.execute('update dhcp set active = 1 where mac = ?', (string[0], ))
                    conn.execute('update dhcp set last_active = ? where mac = ?', (now, string[0]))
                else:
                    query = """insert into dhcp (mac, ip, vlan, interface, switch, active, last_active)
                    values (?, ?, ?, ?, ?, ?, ?)"""
                    conn.execute(query, string + (data_filename[:3], 1, now))
        for last_active in last_active_table:
            if last_active[0] < week_ago:
                conn.execute('delete from dhcp where last_active = ?', (last_active[0], ))


@check_db
def add_into_switches():
    with sqlite3.connect(db_filename) as conn:
        with open('switches.yml', 'r') as f:
            switch_info = yaml.load(f)
            for key, hostname_location_info in switch_info.items():
                for hostname_location in hostname_location_info.items():
                    query = """insert into switches (hostname, location)
                    stringues (?, ?)"""
                    conn.execute(query, hostname_location)

add_into_dhcp()
# add_into_switches()
