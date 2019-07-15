# -*- coding: utf-8 -*-
"""
实现搜索操作
"""
import logging

import requests

from search_tips.util import url


def completion_search(word):
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
                    'size': 20
                }
            }
        }
    })
    names = []
    if r.status_code == 200:
        options = r.json()['suggest']['completion_suggest'][0]['options']
        for option in options:
            names.append(option['_source'])
    else:
        logging.error(r.content)

    return names


def phrase_search(sentence):
    """
    纠错搜索
    :param sentence:
    :return:
    """
    r = requests.post(url + '/_search', json={
        'suggest': {
            'phrase_suggestion': {
                'text': sentence,
                'phrase': {
                    'field': 'suggest_terms.analyzed'
                }
            }
        }
    })
    return map(lambda sug: sug['text'], r.json()['suggest']['phrase_suggestion'])


def term_search(text):
    """
    根据纠错得到的字段进行搜索
    :param text:
    :return:
    """
    r = requests.post(url + '/_search', json={
        'query': {
            'match': {
                'suggest_terms.analyzed': text
            }
        }
    })
    print r.content


if __name__ == '__main__':
    word = 'shangc'

    # 前缀搜索
    result = completion_search(word)
    for res in result:
        print res['name']

    if not result:
        # 错误修正、拼写检查，该功能在中文上的效果非常有限
        texts = phrase_search(word)
        print texts
        for text in texts:
            term_search(text)
