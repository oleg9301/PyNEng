# -*- coding: utf-8 -*-
'''
Задание 14.5

В этом задании соединяется функциональность TextFSM и подключение к оборудованию.

Задача такая:
* подключиться к оборудованию
* выполнить команду show
* полученный вывод передавать на обработку TextFSM
* вернуть результат обработки

Для этого, воспользуемся функциями, которые были созданы ранее:
* функцией send_show_command из упражнения 12.1
* функцией parse_command_dynamic из упражнения 14.4

В этом упражнении нужно создать функцию send_and_parse_command:
* функция должна использовать внутри себя функции parse_command_dynamic и send_show_command.
* какие аргументы должны быть у функции send_and_parse_command, нужно решить самостоятельно
 * но, надо иметь в виду, какие аргументы ожидают две готовые функции, которые мы используем
* функция send_and_parse_command должна возвращать:
 * функция send_show_command возвращает словарь с результатами выполнения команды:
    * ключ - IP устройства
    * значение - результат выполнения команды
 * затем, нужно отправить полученный вывод на обработку функции parse_command_dynamic
 * в результате, должен получиться словарь, в котором:
    * ключ - IP устройства
    * значение - список словарей (то есть, тот вывод, который был получен из функции parse_command_dynamic)

Для функции send_show_command создан файл devices.yaml, в котором находятся параметры подключения к устройствам.

Проверить работу функции send_and_parse_command на команде sh ip int br.
'''
import textfsm.clitable as clitable
import netmiko
import yaml
import getpass

attributes = {'Command': 'show ip interface brief', 'Vendor': 'cisco_ios'}
command = "sh ip int br"
devices = yaml.load(open('devices.yaml'))
username = raw_input('Username: ')
password = getpass.getpass()


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


def send_show_command(device_list, command):
    result = dict()
    for device in device_list['routers']:
        ssh = netmiko.ConnectHandler(username=username, password=password, **device)
        result[device['ip']] = ssh.send_command(command)
    return result


def send_and_parse_command(devices, command, attributes):
    result = dict()
    for device, device_out in send_show_command(devices, command).iteritems():
        result[device] = (parse_command_dynamic(attributes, device_out))
    return result


print(send_and_parse_command(devices, command, attributes))

