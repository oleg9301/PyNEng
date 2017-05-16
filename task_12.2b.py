# -*- coding: utf-8 -*-

'''
Дополнить функцию send_config_commands из задания 12.2a или 12.2

Добавить проверку на ошибки:
* При выполнении команд, скрипт должен проверять результат на такие ошибки:
 * Invalid input detected, Incomplete command, Ambiguous command

Если при выполнении какой-то из команд возникла ошибка,
функция должна выводить сообщение на стандартный поток вывода с информацией
о том, какая ошибка возникла, при выполнении какой команды и на каком устройстве.

Проверить функцию на команде с ошибкой.
'''


import netmiko
import yaml
import getpass


commands = ['logging buffered 64000 debugging',
             'logging trap debugging',
             'log']
devices = yaml.load(open('devices.yaml'))
username = input('Username: ')
password = getpass.getpass()
result = dict()


def send_config_commands(device_list, config_commands):
    for device in device_list['routers']:
        ssh = netmiko.ConnectHandler(username=username, password=password, **device)
        result[device['ip']] = ssh.send_config_set(commands)
        router = result[device['ip']].split('\n')
        indx = [i for i, item in enumerate(router) if item.startswith('% ')]
        if indx:
            print(device['ip'])
            print(router[indx[0]])
            if router[indx[0] - 1].startswith(' '):
                print(router[indx[0] - 2])
            else:
                print(router[indx[0] - 1])
    return result

send_config_commands(devices, commands)
