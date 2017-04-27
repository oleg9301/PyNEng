# -*- coding: utf-8 -*-

'''
Задание 10.3c

С помощью функции draw_topology из файла draw_network_graph.py
сгенерировать топологию, которая соответствует описанию в файле topology.yaml

Обратите внимание на то, какой формат данных ожидает функция draw_topology.
Описание топологии из файла topology.yaml нужно преобразовать соответствующим образом,
чтобы использовать функцию draw_topology.

Для решения задания можно создать любые вспомогательные функции.

В итоге, должно быть сгенерировано изображение топологии.
Результат должен выглядеть так же, как схема в файле task_10_3c_topology.svg

Не копировать код функции draw_topology.

> Для выполнения этого задания, должен быть установлен graphviz:
> pip install graphviz

'''
from draw_network_graph import draw_topology
import yaml
result = {}

with open('topology.yaml', 'r') as f:
    topology = yaml.load(f)

for loc_host, loc_intrf_rem_info in topology.items():
    for loc_intrf, rem_info in loc_intrf_rem_info.items():
        local = (loc_host, loc_intrf)
        for rem_host, rem_intrf in rem_info.items():
            remote = (rem_host, rem_intrf)
            if remote not in result:
                result[local] = remote

draw_topology(result)

