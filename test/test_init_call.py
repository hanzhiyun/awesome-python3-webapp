#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2017-02-18 18:36:51
# @Author  : Han Zhiyun (hanzhiyun1995@qq.com)


class Foo(object):

    def __init__(self):
        print('__init__ executed')

    def __call__(self):
        print('_call__ executed')




Foo() #是什么?
print(isinstance(Foo(),Foo))# 输出啥?
#-----------------------------
Foo()() #输出啥?
#-----------------------------
f = Foo()
f()  #又输出啥?
