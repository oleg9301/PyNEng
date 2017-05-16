# -*- coding: utf-8 -*-

'''
Задание 12.2

Создать функцию send_config_commands

Функция подключается по SSH (с помощью netmiko) к устройствам из списка, и выполняет перечень команд в конфигурационном режиме
на основании переданных аргументов.

Параметры функции:
* devices_list - список словарей с параметрами подключения к устройствам, которым надо передать команды
* config_commands - список команд, которые надо выполнить

Функция возвращает словарь с результатами выполнения команды:
* ключ - IP устройства
* значение - вывод с выполнением команд

Проверить работу функции на примере:
* устройств из файла devices.yaml (для этого надо считать информацию из файла)
* и списка команд commands

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


def send_config_commands(device_list, config_commands):
    for device in device_list['routers']:
        ssh = netmiko.ConnectHandler(username=username, password=password, **device)
        result[device['ip']] = ssh.send_config_set(commands)
    return result

print(send_config_commands(devices, commands))
