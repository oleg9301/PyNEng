# -*- coding: utf-8 -*-

"""
Задание 13.3a

Измените шаблон templates/ospf.txt таким образом, чтобы для перечисленных переменных
были указаны значения по умолчанию, которые используются в том случае,
если переменная не задана.

Не использовать для этого выражения if/else.

Задать в шаблоне значения по умолчанию для таких переменных:
* process - значение по умолчанию 1
* ref_bw - значение по умолчанию 10000


Проверьте получившийся шаблон templates/ospf.txt, на данных в файле data_files/ospf2.yml,
с помощью функции generate_cfg_from_template из задания 13.1-13.1d.
Не копируйте код функции.

"""

import sys
from task_13_1d import generate_cfg_from_template
template_path = sys.argv[1]
data = sys.argv[2]


print(generate_cfg_from_template(template_path, data, trim_blocks=True, lstrip_blocks=True))

