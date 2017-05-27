# -*- coding: utf-8 -*-

"""
Задание 13.1b

Дополнить функцию generate_cfg_from_template из задания 13.1 или 13.1a:
* добавить поддержку аргументов окружения (Environment)

Функция generate_cfg_from_template должна принимать любые аргументы,
которые принимает класс Environment и просто передавать их ему.

Проверить функциональность на аргументах:
* trim_blocks
* lstrip_blocks

"""

from jinja2 import Environment, FileSystemLoader
import yaml
import sys

template_path = sys.argv[1]
vars_file = sys.argv[2]


def generate_cfg_from_template(template_path, vars_file, **arg):
    template_dir, template = template_path.split('/')
    env = Environment(loader=FileSystemLoader(template_dir), **arg)
    template = env.get_template(template)
    vars_dict = yaml.load(open(vars_file))
    return template.render(vars_dict)

print(generate_cfg_from_template(template_path, vars_file, trim_blocks=True, lstrip_blocks=True))

