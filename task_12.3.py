# -*- coding: utf-8 -*-
'''
Задание 12.3

Создать функцию send_commands (для подключения по SSH используется netmiko).

Параметры функции:
* devices_list - список словарей с параметрами подключения к устройствам, которым надо передать команды
* show - одна команда show (строка)
* filename - имя файла, в котором находятся команды, которые надо выполнить (строка)
* config - список с командами, которые надо выполнить в конфигурационном режиме

В зависимости от того, какой аргумент был передан, функция вызывает разные функции внутри.

Далее комбинация из аргумента и соответствующей функции:
* show -- функция send_show_command из задания 12.1
* config -- функция send_config_commands из задания 12.2, 12.2a или 12.2b
* filename -- функция send_commands_from_file (ее также надо написать по аналогии с предыдущими)

Функция возвращает словарь с результатами выполнения команды:
* ключ - IP устройства
* значение - вывод с выполнением команд

Проверить работу функции на примере:
* устройств из файла devices.yaml (для этого надо считать информацию из файла)
* и различных комбинация аргумента с командами:
    * списка команд commands
    * команды command
    * файла config.txt
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
