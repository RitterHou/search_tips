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

    # suggest_terms字段用于term和phrase提示，该提示用于纠错
    data['suggest_terms'] = suggest_values

    # suggest字段用于completion_suggest，该语法用于前缀提示，同时需要字段的type为completion作为配合
    data['suggest'] = []
    for value in suggest_values + [name]:
        completion_suggest = {'input': value}
        if weight and isinstance(weight, int):
            completion_suggest['weight'] = weight
        data['suggest'].append(completion_suggest)

    r = requests.post(url + '/_doc', json=data)
    if r.status_code != 201:
        logging.error('status code is {}'.format(r.status_code))
        logging.error(r.content)


if __name__ == '__main__':
    response = requests.head(url)
    if response.status_code == 404:
        create_index()

    with open('data.txt') as f:
        for line in f.readlines():
            index_data(json.loads(line))
