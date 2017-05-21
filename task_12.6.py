# -*- coding: utf-8 -*-
"""
Задание 12.6

В задании используется пример из раздела про [модуль multiprocessing](book/chapter12/5b_multiprocessing.md).

Переделать пример таким образом, чтобы:
* вместо функции connect_ssh, использовалась функция send_commands из задания 12.3
 * переделать функцию send_commands, чтобы использовалась очередь и функция conn_processes по-прежнему возвращала словарь с результатами.
 * Проверить работу со списком команд, с командами из файла, с командой show


Пример из раздела:
"""

import multiprocessing
import netmiko
import yaml
import getpass


commands = ['logging buffered 64000 debugging',
            'logging trap debugging']
command = "sh ip int br"
username = input('Username: ')
password = getpass.getpass()


def send_show_command(device, show_command):
    result = dict()
    ssh = netmiko.ConnectHandler(username=username, password=password, **device)
    result[device['ip']] = ssh.send_command(show_command)
    return result


def send_config_commands(device, config_commands, output=True):
    result = dict()
    ssh = netmiko.ConnectHandler(username=username, password=password, **device)
    result[device['ip']] = ssh.send_config_set(config_commands)
    if output:
        print(result[device['ip']])
    return result


def send_commands_from_file(device, filename):
    result = dict()
    ssh = netmiko.ConnectHandler(username=username, password=password, **device)
    result[device['ip']] = ssh.send_config_from_file(filename)
    return result


def send_commands(device,  queue, config=[], show='', filename=''):
    if config:
        queue.put(send_config_commands(device, commands, output=False))
    if show:
        queue.put(send_show_command(device, show))
    if filename:
        queue.put(send_commands_from_file(device, filename))


def conn_processes(function, devices, config=[], show='', filename=''):
    processes = []
    queue = multiprocessing.Queue()

    for device in devices:
        p = multiprocessing.Process(target=function, args=(device, queue, config, show, filename))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    results = dict()
    for p in processes:
        results.update(queue.get())

    return results

devices = yaml.load(open('devices.yaml'))['routers']

print(conn_processes(send_commands, devices, config=commands))
print('\n')
print(conn_processes(send_commands, devices, show=command))
print('\n')
print(conn_processes(send_commands, devices, filename='config.txt'))
