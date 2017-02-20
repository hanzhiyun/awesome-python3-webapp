#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2017-02-17 11:21:22
# @Author  : Han Zhiyun (hanzhiyun1995@qq.com)
import asyncio,time
import sys
sys.path.append("..")
from www import orm
from www.models import User, Blog, Comment

# def test():
# yield from orm.create_pool(user='www-data', password='www-data',
# database='awesome')

#     u = User(name='Test', email='test@example.com', passwd='1234567890', image='about:blank')

#     yield from u.save()

# for x in test():
#     pass

if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    @asyncio.coroutine
    def test():

        yield from orm.create_pool(loop=loop, host='localhost', port=3306, user='www-data', password='74527452', db='awesome')
        # u = User(name='hby', email='hubayi@gmail.com', passwd='74558456', image='about:blank', admin=True)
        summary = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'
        u1 = Blog(user_id='1', user_image='about:blank', user_name='hby', content='测试', name='Test Blog', summary=summary, created_at=time.time()-120)
        u2 = Blog(user_id='2', user_image='about:blank', user_name='hby', content='测试', name='Something New', summary=summary, created_at=time.time()-3600)
        u3 = Blog(user_id='3', user_image='about:blank', user_name='hby', content='测试', name='Learn Swift', summary=summary, created_at=time.time()-7200)

        yield from u1.save()
        yield from u2.save()
        yield from u3.save()

        yield from orm.destroy_pool()

    loop.run_until_complete(test())
    loop.close()
    if loop.is_closed():
        sys.exit(0)
