# -*- coding: utf-8 -*-
"""
实现搜索操作
"""
import logging

import requests

from search_tips.util import url


def search(word):
    """
    前缀搜索
    :param word:
    :return:
    """
    r = requests.post(url + '/_search', json={
        'suggest': {
            'completion_suggest': {
                'prefix': word,
                'completion': {
                    'field': 'suggest',
                    'size': 10
                }
            }
        }
    })
    names = []
    if r.status_code == 200:
        options = r.json()['suggest']['completion_suggest'][0]['options']
        map(lambda option: names.append(option['_source']), options)
    else:
        logging.error(r.content)

    return names


if __name__ == '__main__':
    result = search('kafeil')
    for res in result:
        print res['name']
