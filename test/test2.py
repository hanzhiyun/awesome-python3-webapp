#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2017-02-16 16:54:44
# @Author  : Han Zhiyun (hanzhiyun1995@qq.com)


def greet_me(**fuckhahah):
    for key, value in my_info.items():
        print("{0} ==&gt; {1}".format(key, value))
        print(my_info.get(key))
        print('Fuck','None')
my_info={'name':'sly','email':'slysly759@gmail.com'}
greet_me(**my_info)
# print(my_info.items())