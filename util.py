# -*- coding: utf-8 -*-
"""
一些常量以及创建索引的方法
"""
import logging
import sys

import requests
from pypinyin import pinyin, NORMAL, FIRST_LETTER, INITIALS

logging.basicConfig(level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S',
                    format='%(asctime)s - %(levelname)5s - %(message)s', stream=sys.stdout)

url = 'http://127.0.0.1:9200/products'


def word_2_pinyin(input_str):
    """
    汉字转化为拼音
    :param input_str:
    :return:
    """

    def combine_word(word_list):
        size = 0
        for words in word_list:
            if size == 0:
                size += len(words)
            else:
                size *= len(words)

        result = [''] * size
        for words in word_list:
            for i in xrange(size):
                result[i] += words[i % len(words)]
        return result

    if isinstance(input_str, str):
        input_str = input_str.decode('utf-8')

    # 得到三种拼音风格
    normal = pinyin(input_str, style=NORMAL, heteronym=True)
    first_letter = pinyin(input_str, style=FIRST_LETTER, heteronym=True)
    initials = pinyin(input_str, style=INITIALS, heteronym=True)
    return list(set(combine_word(normal) + combine_word(first_letter) + combine_word(initials)))


def create_index():
    """
    创建索引
    :return:
    """
    r = requests.put(url, json={
        'settings': {
            'index': {
                'number_of_shards': 1,
                'number_of_replicas': 0
            }
        },
        'mappings': {
            'dynamic_templates': [
                {
                    'strings': {
                        'match_mapping_type': 'string',
                        'mapping': {
                            'type': 'keyword',
                            'fields': {
                                'analyzed': {
                                    'type': 'text',
                                    'analyzer': 'ik_max_word'
                                }
                            }
                        }
                    }
                }
            ],
            'properties': {
                'suggest': {
                    'type': 'completion'
                }
            }
        }
    })
    if r.status_code != 200:
        logging.error(r.content)

    logging.info('{} create_index_success'.format(url))
