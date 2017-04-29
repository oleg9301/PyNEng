# -*- coding: utf-8 -*-

"""
Задание 11.1a

Добавить в файл add_data.py, из задания 11.1, проверку на наличие БД:
* если файл БД есть, записать данные
* если файла БД нет, вывести сообщение, что БД нет и её необходимо сначала создать

"""

import sqlite3
import re
import glob
import yaml
import os
import sys


db_filename = 'dhcp_snooping.db'
schema_filename = 'dhcp_snooping_schema.sql'
dhcp_snoop_files = glob.glob('sw*_dhcp_snooping.txt')
regex = re.compile('(.+?) +(.*?) +\d+ +[\w-]+ +(\d+) +(.*$)')
db_exists = os.path.exists(db_filename)


def check_db(func):
    def check_info():
        if not db_exists:
            sys.exit('Database does not exists. Please create dhcp_snooping.db')
        func()
    return check_info


@check_db
def add_into_dhcp():
    with sqlite3.connect(db_filename) as conn:
        for data_filename in dhcp_snoop_files:
            with open(data_filename) as data:
                result = [regex.search(line).groups() for line in data if line[0].isdigit()]
            for val in result:
                query = """insert into dhcp (mac, ip, vlan, interface, switch)
                values (?, ?, ?, ?, ?)"""
                conn.execute(query, val + (data_filename[:3],))


@check_db
def add_into_switches():
    with sqlite3.connect(db_filename) as conn:
        with open('switches.yml', 'r') as f:
            switch_info = yaml.load(f)
            for key, hostname_location_info in switch_info.items():
                for hostname_location in hostname_location_info.items():
                    query = """insert into switches (hostname, location)
                    values (?, ?)"""
                    conn.execute(query, hostname_location)

add_into_dhcp()
add_into_switches()
