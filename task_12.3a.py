# -*- coding: utf-8 -*-
'''
Задание 12.3a


Изменить функцию send_commands таким образом, чтобы в списке словарей device_list
не надо было указывать имя пользователя, пароль, и пароль на enable.

Функция должна запрашивать имя пользователя, пароль и пароль на enable при старте.
Пароль не должен отображаться при наборе.

В файле devices2.yaml эти параметры уже удалены.
'''
import netmiko
import yaml
import getpass


commands = ['logging buffered 64000 debugging',
            'logging trap debugging']
command = "sh ip int br"
username = input('Username: ')
password = getpass.getpass()


def send_show_command(device_list, show_command):
    result = dict()
    for device in device_list:
        ssh = netmiko.ConnectHandler(username=username, password=password, **device)
        result[device['ip']] = ssh.send_command(show_command)
    return result


def send_config_commands(device_list, config_commands, output=True):
    result = dict()
    for device in device_list:
        ssh = netmiko.ConnectHandler(username=username, password=password, **device)
        result[device['ip']] = ssh.send_config_set(config_commands)
        if output:
            print(result[device['ip']])
    return result


def send_commands_from_file(device_list, filename):
    result = dict()
    for device in device_list:
        ssh = netmiko.ConnectHandler(username=username, password=password, **device)
        result[device['ip']] = ssh.send_config_from_file(filename)
    return result


def send_commands(device_list='devices.yaml', config=[], show='', filename=''):
    device_list = yaml.load(open(device_list))['routers']
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
