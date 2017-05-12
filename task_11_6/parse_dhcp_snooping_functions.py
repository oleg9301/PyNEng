# -*- coding: utf-8 -*-
import os
import re
import yaml
import sqlite3
from datetime import datetime, timedelta

regex = re.compile('(.+?) +(.*?) +\d+ +[\w-]+ +(\d+) +(.*$)')
now = str(datetime.today().replace(microsecond=0))
week_ago = str(datetime.today().replace(microsecond=0) - timedelta(days=7))


def create_db(db_filename, schema_filename):
    db_exists = os.path.exists(db_filename)
    with sqlite3.connect(db_filename) as conn:
        if not db_exists:
            print('Creating schema...')
            with open(schema_filename, 'r') as f:
                schema = f.read()
            conn.executescript(schema)
            print('Done')
        else:
            print('Database exists, assume dhcp table does, too.')


def add_data_switches(db_filename, yml_filename):
    with sqlite3.connect(db_filename) as conn:
        current_switch_table = conn.execute('select hostname from switches').fetchall()
        with open(yml_filename[0], 'r') as f:
            switch_info = yaml.load(f)
            for key, hostname_location_info in switch_info.items():
                for hostname_location in hostname_location_info.items():
                    if (hostname_location[0], ) not in current_switch_table:
                        query = """insert into switches (hostname, location)
                        values (?, ?)"""
                        conn.execute(query, hostname_location)


def add_data(db_filename, dhcp_snoop_files):
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


def get_data(db_filename, key, value):
    keys = ['mac', 'ip', 'vlan', 'interface']
    keys.remove(key)
    with sqlite3.connect(db_filename) as conn:
        conn.row_factory = sqlite3.Row
        for act in (1, 0):
            if act == 0:
                print("Inactive values:", '\n' + '-' * 40)
            else:
                print("\nDetailed information for host(s) with", key, value, '\n' + '-' * 40)
            result = conn.execute("select * from dhcp where {} = ? and active = ?".format(key), (value, act))
            for row in result:
                for k in keys:
                    print("{:12}: {}".format(k, row[k]))
                print('-' * 40)


def get_all_data(db_filename):
    with sqlite3.connect(db_filename) as conn:
        print('В таблице dhcp такие записи:', '\n' + '-' * 40)
        query = "select * from dhcp"
        result = conn.execute(query)
        for column in result:
            print("%-20s %-18s %-5s %-18s %-4s %-2s %-20s" % column)

