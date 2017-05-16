# -*- coding: utf-8 -*-
'''
Задание 12.1

Создать функцию send_show_command.

Функция подключается по SSH (с помощью netmiko) к устройствам из списка, и выполняет  команду
на основании переданных аргументов.

Параметры функции:
* devices_list - список словарей с параметрами подключения к устройствам, которым надо передать команды
* command - команда, которую надо выполнить

Функция возвращает словарь с результатами выполнения команды:
* ключ - IP устройства
* значение - результат выполнения команды

Проверить работу функции на примере:
* устройств из файла devices.yaml (для этого надо считать информацию из файла)
* и команды command

'''

import netmiko
import yaml
import getpass

command = "sh ip int br"
devices = yaml.load(open('devices.yaml'))
username = input('Username: ')
password = getpass.getpass()
result = dict()


def send_show_command(device_list, command):
    for device in device_list['routers']:
        ssh = netmiko.ConnectHandler(username=username, password=password, **device)
        result[device['ip']] = ssh.send_command(command)
    return result

print(send_show_command(devices, command))
