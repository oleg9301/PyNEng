# -*- coding: utf-8 -*-

"""
Задание 11.1

* add_data.py
 * с помощью этого скрипта, мы будем добавлять данные в БД
  * теперь у нас есть не только данные из вывода sh ip dhcp snooping binding,
    но и информация о коммутаторах

Соответственно, в файле add_data.py у нас будет две части:
* запись информации о коммутаторах в таблицу switches
 * данные о коммутаторах, находятся в файле switches.yml
* запись информации на основании вывода sh ip dhcp snooping binding
 * теперь у нас есть вывод с трёх коммутаторов:
   * файлы sw1_dhcp_snooping.txt, sw2_dhcp_snooping.txt, sw3_dhcp_snooping.txt
 * так как таблица dhcp изменилась, и в ней теперь присутствует поле switch,
   нам нужно его заполнять. Имя коммутатора мы определяем по имени файла с данными

"""
import sqlite3
import re
import glob
import yaml


db_filename = 'dhcp_snooping.db'
schema_filename = 'dhcp_snooping_schema.sql'
dhcp_snoop_files = glob.glob('sw*_dhcp_snooping.txt')
regex = re.compile('(.+?) +(.*?) +\d+ +[\w-]+ +(\d+) +(.*$)')


def add_into_dhcp():
    with sqlite3.connect(db_filename) as conn:
        for data_filename in dhcp_snoop_files:
            with open(data_filename) as data:
                result = [regex.search(line).groups() for line in data if line[0].isdigit()]
            for val in result:
                query = """insert into dhcp (mac, ip, vlan, interface, switch)
                values (?, ?, ?, ?, ?)"""
                conn.execute(query, val + (data_filename[:3],))


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
