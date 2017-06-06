# -*- coding: utf-8 -*-
'''
Задание 14.6

Это задание похоже на задание 14.5, но в этом задании подключения надо выполнять параллельно.

Для этого надо использовать функции connect_ssh и conn_processes (пример из раздела multiprocessing) и функцию parse_command_dynamic из упражнения 14.4.

В этом упражнении нужно создать функцию send_and_parse_command_parallel:
* она должна использовать внутри себя функции connect_ssh, conn_processes и parse_command_dynamic
* какие аргументы должны быть у функции send_and_parse_command_parallel, нужно решить самостоятельно
 * но надо иметь в виду, какие аргументы ожидают три готовые функции, которые используются
* функция send_and_parse_command_parallel должна возвращать словарь, в котором:
 * ключ - IP устройства
 * значение - список словарей (то есть, тот вывод, который был получен из функции parse_command_dynamic)

Для функции conn_processes создан файл devices.yaml, в котором находятся параметры подключения к устройствам.

Проверить работу функции send_and_parse_command_parallel на команде sh ip int br.

Пример из раздела multiprocessing:
'''

import multiprocessing
import yaml
import textfsm.clitable as clitable
import netmiko
import getpass

attributes = {'Command': 'show ip interface brief', 'Vendor': 'cisco_ios'}
command = "sh ip int br"
devices = yaml.load(open('devices.yaml'))['routers']
username = raw_input('Username: ')
password = getpass.getpass()


def connect_ssh(device, command, queue):
    ssh = netmiko.ConnectHandler(username=username, password=password, **device)
    queue.put({device['ip']: ssh.send_command(command)})


def conn_processes(function, devices, command):
    processes = []
    queue = multiprocessing.Queue()
    for device in devices:
        p = multiprocessing.Process(target=function, args=(device, command, queue))
        p.start()
        processes.append(p)
    for p in processes:
        p.join()
    result = []
    for p in processes:
        result.append(queue.get())
    return result


def parse_command_dynamic(attributes, output, index='index', templates='templates'):
    cli_table = clitable.CliTable(index, templates)
    cli_table.ParseCmd(output, attributes)
    data_rows = []
    for row in cli_table:
        current_row = []
        for value in row:
            current_row.append(value)
        data_rows.append(current_row)
    header = []
    map(header.append, cli_table.header)
    result = []
    for row in data_rows:
        result.append(dict(zip(header, row)))
    return result


def send_and_parse_command_parallel(devices, command, attributes):
    result = dict()
    for device in conn_processes(connect_ssh, devices, command):
        for device_ip, device_out in device.iteritems():
            result[device_ip] = (parse_command_dynamic(attributes, device_out))
    return result

print(send_and_parse_command_parallel(devices, command, attributes))

