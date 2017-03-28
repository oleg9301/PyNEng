# -*- coding: utf-8 -*-

'''
Задание 9.3b

Проверить работу функции parse_cfg из задания 9.3a на конфигурации config_r2.txt.

Обратите внимание, что на интерфейсе e0/1 назначены два IP-адреса:
interface Ethernet0/1
 ip address 10.255.2.2 255.255.255.0
 ip address 10.254.2.2 255.255.255.0 secondary

А в словаре, который возвращает функция parse_cfg, интерфейсу Ethernet0/1
соответствует только один из них (второй).

Переделайте функцию parse_cfg из задания 9.3a таким образом,
чтобы она возвращала список кортежей для каждого интерфейса.
Если на интерфейсе назначен только один адрес, в списке будет один кортеж.
Если же на интерфейсе настроены несколько IP-адресов, то в списке будет несколько кортежей.

Проверьте функцию на конфигурации config_r2.txt и убедитесь, что интерфейсу
Ethernet0/1 соответствует список из двух кортежей.
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
                    if interface in result:
                        result[interface].append(tuple(x for x in regex_ip_match))
                    else:
                        result[interface] = [tuple(x for x in regex_ip_match)]
    except OSError:
        print('File {} not found'.format(file_name))
    return result

print(parse_cfg('config_r2.txt'))
