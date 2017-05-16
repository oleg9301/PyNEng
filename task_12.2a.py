# -*- coding: utf-8 -*-
'''
Задание 12.2a

Дополнить функцию send_config_commands из задания 12.2

Добавить аргумент output, который контролирует будет ли результат выполнения команд выводится на стандартный поток вывода.
По умолчанию, результат должен выводиться.
'''


import netmiko
import yaml
import getpass

commands = ['logging buffered 64000 debugging',
             'logging trap debugging',
             'logging facility local4']
devices = yaml.load(open('devices.yaml'))
username = input('Username: ')
password = getpass.getpass()
result = dict()


def send_config_commands(device_list, config_commands, output=True):
    for device in device_list['routers']:
        ssh = netmiko.ConnectHandler(username=username, password=password, **device)
        result[device['ip']] = ssh.send_config_set(commands)
        if output:
            print(result[device['ip']])
    return result

send_config_commands(devices, commands)
