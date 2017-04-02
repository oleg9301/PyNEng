# -*- coding: utf-8 -*-

'''
Задание 10.1

В этом задании нужно:
* взять содержимое нескольких файлов с выводом команды sh version
* распарсить вывод команды с помощью регулярных выражений и получить информацию об устройстве
* записать полученную информацию в файл в CSV формате

Для выполнения задания нужно создать две функции.

Функция parse_sh_version:
* ожидает аргумент output в котором находится вывод команды sh version
* обрабатывает вывод, с помощью регулярных выражений
* возвращает кортеж из трёх элементов:
 * ios - в формате "12.4(5)T"
 * image - в формате "flash:c2800-advipservicesk9-mz.124-5.T.bin"
 * uptime - в формате "5 days, 3 hours, 3 minutes"

Функция write_to_csv:
* ожидает два аргумента:
 * имя файла, в который будет записана информация в формате CSV
 * данные в виде списка списков, где:
    * первый список - заголовки столбцов,
    * остальные списки - содержимое
* функция записывает содержимое в файл, в формате CSV и ничего не возвращает

Остальное содержимое скрипта может быть в скрипте, а может быть в ещё одной функции.

Скрипт должен:
* обработать информацию из каждого файла с выводом sh version:
 * sh_version_r1.txt, sh_version_r2.txt, sh_version_r3.txt
* с помощью функции parse_sh_version, из каждого вывода должна быть получена информация ios, image, uptime
* из имени файла нужно получить имя хоста
* после этого вся информация должна быть записана в файл routers_inventory.csv

В скрипте, с помощью модуля glob, создан список файлов, имя которых начинается на sh_vers.
Вы можете раскомментировать строку print sh_version_files, чтобы посмотреть содержимое списка.

Кроме того, создан список заголовков (headers), который должен быть записан в CSV.
'''

import glob
import re
import csv
import sys

sh_version_files = glob.glob('sh_vers*')
regex_ios = re.compile('Cisco IOS Software.*?Version\s(.*?),')
regex_image = re.compile('System image file is (.*)')
regex_uptime = re.compile('uptime is (.*)')
regex_hostname = re.compile('sh_version_(.*?)\.txt')
sh_ver_list = [['hostname', 'ios', 'image', 'uptime']]


def parse_sh_version(output):
    try:
        ios = re.search(regex_ios, output).group(1)
        image = re.search(regex_image, output).group(1)
        uptime = re.search(regex_uptime, output).group(1)
    except AttributeError:
        print('Wrong file {}'.format(file))
        sys.exit()
    return (ios, image, uptime)


def write_to_csv(csv_file_name, sh_ver_list):
    try:
        with open(csv_file_name, 'w') as f:
            writer = csv.writer(f)
            for row in sh_ver_list:
                writer.writerow(row)
    except OSError:
        print('File {} cant be open/write'.format(csv_file_name))
        sys.exit()

for file in sh_version_files:
    try:
        with open(file, 'r') as f:
            file_string = f.read().strip()
            hostname = re.search(regex_hostname, file).group(1)
            sh_ver_list.append([hostname] + list(parse_sh_version(file_string)))
    except OSError:
        print('File {} cant be open/read'.format(file))
        sys.exit()
write_to_csv('routers_inventory.csv', sh_ver_list)
