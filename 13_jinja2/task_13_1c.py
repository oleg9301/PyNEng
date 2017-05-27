# -*- coding: utf-8 -*-

"""
Задание 13.1c

Дополнить функцию generate_cfg_from_template из задания 13.1, 13.1a или 13.1b:
* добавить поддержку разных форматов для файла с данными

Должны поддерживаться такие форматы:
* YAML
* JSON
* словарь Python

Сделать для каждого формата свой параметр функции.
Например:
* YAML - yaml_file
* JSON - json_file
* словарь Python - py_dict

Проверить работу функции на шаблоне templates/for.txt и данных:
* data_files/for.yml
* data_files/for.json
* словаре data_dict

"""
from jinja2 import Environment, FileSystemLoader
import yaml
import json
import sys

data_dict = {'vlans': {
                        10: 'Marketing',
                        20: 'Voice',
                        30: 'Management'},
             'ospf': [{'network': '10.0.1.0 0.0.0.255', 'area': 0},
                      {'network': '10.0.2.0 0.0.0.255', 'area': 2},
                      {'network': '10.1.1.0 0.0.0.255', 'area': 0}],
             'id': 3,
             'name': 'R3'}


template_path = sys.argv[1]
vars_file = sys.argv[2]


def generate_cfg_from_template(template_path, yaml_file=None, json_file=None, py_dict=None, **arg):
    template_dir, template = template_path.split('/')
    env = Environment(loader=FileSystemLoader(template_dir), **arg)
    template = env.get_template(template)
    if yaml_file:
        vars_dict = yaml.load(open(vars_file))
    if json_file:
        vars_dict = json.load(open(vars_file))
    if py_dict:
        vars_dict = py_dict
    return template.render(vars_dict)

print(generate_cfg_from_template(template_path, py_dict=data_dict, trim_blocks=True, lstrip_blocks=True))

