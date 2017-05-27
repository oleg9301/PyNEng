# -*- coding: utf-8 -*-

"""
Задание 13.1

Переделать скрипт cfg_gen.py в функцию generate_cfg_from_template.

Функция ожидает два аргумента:
* путь к шаблону
* файл с переменными в формате YAML

Функция должна возвращать конфигурацию, которая была сгенерирована.

Проверить работу функции на шаблоне templates/for.txt и данных data_files/for.yml.

"""

from jinja2 import Environment, FileSystemLoader
import yaml
import sys

template_path = sys.argv[1]
vars_file = sys.argv[2]


def generate_cfg_from_template(template_path, vars_file):
    template_dir, template = template_path.split('/')
    env = Environment(loader=FileSystemLoader(template_dir), trim_blocks=True)
    template = env.get_template(template)
    vars_dict = yaml.load(open(vars_file))
    return template.render(vars_dict)

print(generate_cfg_from_template(template_path, vars_file))
