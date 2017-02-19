#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2017-02-19 09:49:55
# @Author  : Han Zhiyun (hanzhiyun1995@qq.com)

'''
Default configurations.
'''

configs = {
	'debug': True,
    'db': {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'www-data',
        'password': '74527452',
        'db': 'awesome'
    },
    'session': {
        'secret': 'Awesome'
    }
}
