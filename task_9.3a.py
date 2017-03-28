# -*- coding: utf-8 -*-

'''
Задание 9.3a

Переделать функцию parse_cfg из задания 9.3 таким образом, чтобы она возвращала словарь:
* ключ: имя интерфейса
* значение: кортеж с двумя строками:
  * IP-адрес
  * маска

Например (взяты произвольные адреса):
{'FastEthernet0/1':('10.0.1.1', '255.255.255.0'),
 'FastEthernet0/2':('10.0.2.1', '255.255.255.0')}

Для получения такого результата, используйте регулярные выражения.

Проверить работу функции на примере файла config_r1.txt.
'''


from re import findall


def parse_cfg(file_name):
    result = {}
    regex_ip = '(\d+\.\d+\.\d+\.\d+)'
    try:
        with open(file_name, 'r') as f:
            file_string = f.read().strip().split('\n')
            for string in file_string:
                if string[:9] == 'interface' and string[-1].isdigit:
                    interface = (string.split()[1])
                regex_ip_match = findall(regex_ip, string)
                if regex_ip_match and 'address' in string:
                    result[interface] = tuple(x for x in regex_ip_match)
    except OSError:
        print('File {} not found'.format(file_name))
    return result

print(parse_cfg('config_r1.txt'))
