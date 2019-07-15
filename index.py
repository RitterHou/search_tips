# -*- coding: utf-8 -*-
"""
索引数据
"""
import json
import logging

import requests

from search_tips.util import url, word_2_pinyin, create_index


def index_data(data, weight=None):
    """
    索引数据到ES
    :param data:
    :param weight:
    :return:
    """
    name = data.get('name')
    if not name:
        logging.error('can\'t find name field')
        return

    suggest_values = word_2_pinyin(name)

    data['suggest'] = []
    for value in suggest_values + [name]:
        suggest = {'input': value}
        if weight and isinstance(weight, int):
            suggest['weight'] = weight
        data['suggest'].append(suggest)

    # 写入数据
    r = requests.post(url + '/_doc', json=data)
    if r.status_code != 201:
        logging.error('status code is {}'.format(r.status_code))
        logging.error(r.content)


if __name__ == '__main__':
    response = requests.head(url)
    if response.status_code == 404:
        create_index()

    f = open('data.txt')
    for line in f.readlines():
        index_data(json.loads(line))
    f.close()
