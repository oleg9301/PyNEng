# -*- coding: utf-8 -*-

"""
Задание 13.1a

Переделать функцию generate_cfg_from_template:
* добавить поддержку использования шаблона, который находится в текущем каталоге

Для проверки, скопируйте один из шаблонов из каталога templates,
в текущий каталог скрипта.

Можно проверить на тех же шаблоне и данных, что и в прошлом задании:
* шаблоне templates/for.txt (но скопировать его в текущий каталог) и данных data_files/for.yml

"""

from jinja2 import Environment, FileSystemLoader
import yaml
import sys

template_path = sys.argv[1]
vars_file = sys.argv[2]


def generate_cfg_from_template(template_path, vars_file):
    if '/' in template_path:
        template_dir, template = template_path.split('/')
        env = Environment(loader=FileSystemLoader(template_dir), trim_blocks=True)
    else:
        template = template_path
        env = Environment(loader=FileSystemLoader('.'), trim_blocks=True)
    template = env.get_template(template)
    vars_dict = yaml.load(open(vars_file))
    return template.render(vars_dict)

print(generate_cfg_from_template(template_path, vars_file))

