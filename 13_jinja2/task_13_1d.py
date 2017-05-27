# -*- coding: utf-8 -*-

"""
Задание 13.1d

Переделать функцию generate_cfg_from_template из задания 13.1, 13.1a, 13.1b или 13.1c:
* сделать автоматическое распознавание разных форматов для файла с данными
* для передачи разных типов данных, должен использоваться один и тот же параметр data

Должны поддерживаться такие форматы:
* YAML - файлы с расширением yml или yaml
* JSON - файлы с расширением json
* словарь Python

Если не получилось определить тип данных, вывести сообщение error_message (перенести текст сообщения в тело функции), завершить работу функции и вернуть None.

Проверить работу функции на шаблоне templates/for.txt и данных:
* data_files/for.yml
* data_files/for.json
* словаре data_dict

"""
from jinja2 import Environment, FileSystemLoader
import yaml
import json
import sys
import textwrap


data_dict = {'vlans': {
                        10: 'Marketing',
                        20: 'Voice',
                        30: 'Management'},
             'ospf': [{'network': '10.0.1.0 0.0.0.255', 'area': 0},
                      {'network': '10.0.2.0 0.0.0.255', 'area': 2},
                      {'network': '10.1.1.0 0.0.0.255', 'area': 0}],
             'id': 3,
             'name': 'R3'}


def generate_cfg_from_template(template_path, data, **arg):
    error_message = textwrap.dedent("""\
                    Не получилось определить формат данных.
                    Поддерживаются файлы с расширением .json, .yml, .yaml и словари Python
                    """)
    template_dir, template = template_path.split('/')
    env = Environment(loader=FileSystemLoader(template_dir), **arg)
    template = env.get_template(template)
    if type(data) is dict:
        vars_dict = data
    elif 'yml' in data or 'yaml' in data:
        vars_dict = yaml.load(open(data))
    elif 'json' in data:
        vars_dict = json.load(open(data))
    else:
        return error_message
    return template.render(vars_dict)

if __name__ == '__main__':
    template_path = sys.argv[1]
    vars_file = sys.argv[2]
    print(generate_cfg_from_template(template_path, data=vars_file, trim_blocks=True, lstrip_blocks=True))
