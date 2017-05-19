# -*- coding: utf-8 -*-
'''
Задание 12.3b


Дополнить функцию send_commands таким образом, чтобы перед подключением к устройствам по SSH,
выполнялась проверка доступности устройства pingом (можно вызвать команду ping в ОС).

> Как выполнять команды ОС, описано в разделе [subprocess](https://natenka.gitbooks.io/pyneng/content/book/16_additional_info/useful_modules/subprocess.html). Там же есть пример функции с отправкой ping.

Если устройство доступно, можно выполнять подключение.
Если не доступно, вывести сообщение о том, что устройство с определенным IP-адресом недоступно
и не выполнять подключение.

Для удобства можно сделать отдельную функцию для проверки доступности
и затем использовать ее в функции send_commands.
'''

import netmiko
import yaml
import getpass
import os


commands = ['logging buffered 64000 debugging',
            'logging trap debugging']
command = "sh ip int br"
username = input('Username: ')
password = getpass.getpass()
result = dict()


def send_show_command(device_list, show_command):
    for device in device_list:
        ssh = netmiko.ConnectHandler(username=username, password=password, **device)
        result[device['ip']] = ssh.send_command(show_command)
    return result


def send_config_commands(device_list, config_commands, output=True):
    for device in device_list:
        ssh = netmiko.ConnectHandler(username=username, password=password, **device)
        result[device['ip']] = ssh.send_config_set(config_commands)
        if output:
            print(result[device['ip']])
    return result


def send_commands_from_file(device_list, filename):
    for device in device_list:
        ssh = netmiko.ConnectHandler(username=username, password=password, **device)
        result[device['ip']] = ssh.send_config_from_file(filename)
    return result


def send_commands(device_list='devices.yaml', config=[], show='', filename=''):
    device_list = yaml.load(open(device_list))['routers']
    for device in device_list:
        if os.system('ping -c 1 ' + device['ip'] + '>>/dev/null') != 0:
            print('device with ip ' + device['ip'] + 'is unavailable.')
            device_list.remove(device)
    if config:
        return send_config_commands(device_list, commands, output=False)
    if show:
        return send_show_command(device_list, show)
    if filename:
        return send_commands_from_file(device_list, filename)

print(send_commands(config=commands))
print('\n')
print(send_commands(show=command))
print('\n')
print(send_commands(filename='config.txt'))
