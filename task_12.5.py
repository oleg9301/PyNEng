# -*- coding: utf-8 -*-
'''
Задание 12.5

Использовать функции полученные в результате выполнения задания 12.4.

Переделать функцию conn_threads таким образом, чтобы с помощью аргумента limit,
можно было указывать сколько подключений будут выполняться параллельно.
По умолчанию, значение аргумента должно быть 2.

Изменить функцию соответственно, так, чтобы параллельных подключений выполнялось столько,
сколько указано в аргументе limit.

'''


import threading
import queue
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


def conn_threads(function, devices, config=[], show='', filename='', limit=2):
    threads = []
    q = queue.Queue()

    count = 0
    for device in devices:
        th = threading.Thread(target=function, args=(device, q, config, show, filename))
        th.start()
        threads.append(th)
        if count < limit:
            continue
        else:
            for th in threads:
                th.join()
            count = 0
    for th in threads:
        th.join()

    results = dict()
    for t in threads:
        results.update(q.get())

    return results

devices = yaml.load(open('devices.yaml'))['routers']

print(conn_threads(send_commands, devices, config=commands))
print('\n')
print(conn_threads(send_commands, devices, show=command))
print('\n')
print(conn_threads(send_commands, devices, filename='config.txt'))
