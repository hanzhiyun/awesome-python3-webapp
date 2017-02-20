#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2017-02-18 19:05:40
# @Author  : Han Zhiyun (hanzhiyun1995@qq.com)

import re
import time
import json
import logging
import hashlib
import base64
import asyncio
import markdown2
from coroweb import get, post
from aiohttp import web
from models import User, Comment, Blog, next_id
from apis import APIValueError, APIResourceNotFoundError
from config import configs


COOKIE_NAME = 'awesession'
_COOKIE_KEY = configs.session.secret


def user2cookie(user, max_age):
    '''
    Generate cookie str by user.
    '''
    # build cookie string by: id-expires-sha1
    expires = str(int(time.time() + max_age))
    s = '%s-%s-%s-%s' % (user.id, user.passwd, expires, _COOKIE_KEY)
    L = [user.id, expires, hashlib.sha1(s.encode('utf-8')).hexdigest()]
    return '-'.join(L)


@asyncio.coroutine
def cookie2user(cookie_str):
    '''
    Parse cookie and load user if cookie is valid.
    '''
    if not cookie_str:
        return None
    try:
        L = cookie_str.split('-')
        if len(L) != 3:
            return None
        uid, expires, sha1 = L
        if int(expires) < time.time():
            return None
        user = yield from User.find(uid)
        if user is None:
            return None
        s = '%s-%s-%s-%s' % (uid, user.passwd, expires, _COOKIE_KEY)
        if sha1 != hashlib.sha1(s.encode('utf-8')).hexdigest():
            logging.info('invalid sha1')
            return None
        user.passwd = '******'
        return user
    except Exception as e:
        logging.exception(e)
        return None

'''
@get('/blog')
async def handler_url_blog(request):
    body = '<h1>Awesome: /blog</h1>'
    return body


@get('/greeting')
async def handler_url_greeting(*, name, request):
    body = '<h1>Awesome: /greeting %s</h1>' % name
    return body


@get('/input')
async def handler_url_input(request):
    body = '<form action="/result" method="post">E-mail: <input type="email" name="user_email" /><input type="submit" /></form>'
    return body


@post('/result')
async def handler_url_result(*, user_email, request):
    body = '<h1>您输入的邮箱是%s</h1>' % user_email
    return body


@get('/index')
async def handler_url_index(request):
    body = '<h1>Awesome: /index</h1>'
    return body


@get('/create_comment')
async def handler_url_create_comment(request):
    body = '<h1>Awesome: /create_comment</h1>'
    return body
'''

'''
@get('/')
async def index(request):
    users = await User.findAll()
    return {
        '__template__': 'test.html',
        'users': users
    }
'''


@get('/register')
def register():
    return {
        '__template__': 'register.html'
    }


@get('/signin')
def signin():
    return {
        '__template__': 'signin.html'
    }


@get('/signout')
def signout(request):
    referer = request.headers.get('Referer')
    r = web.HTTPFound(referer or '/')
    r.set_cookie(COOKIE_NAME, '-deleted-', max_age=0, httponly=True)
    logging.info('user signed out.')
    return r


@get('/')
async def index(request):
    # summary = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'
    # blogs = [
    #     Blog(id='1', name='Test Blog', summary=summary, created_at=time.time()-120),
    #     Blog(id='2', name='Something New', summary=summary, created_at=time.time()-3600),
    #     Blog(id='3', name='Learn Swift', summary=summary, created_at=time.time()-7200)
    # ]
    blogs = await Blog.findAll()
    return {
        '__template__': 'blogs.html',
        'blogs': blogs,
        '__user__': request.__user__
    }


@get('/api/users')
async def api_get_users():
    users = await User.find_All(orderBy='created_at desc')
    for u in users:
        u.passwd = '******'
    return dict(users=users)

# @get('/api/users')
# def api_get_users(*, page='1'):
#     page_index = get_page_index(page)
#     num = yield from User.findNumber('count(id)')
#     p = Page(num, page_index)
#     if num == 0:
#         return dict(page=p, users=())
#     users = yield from User.findAll(orderBy='created_at desc', limit=(p.offset, p.limit))
#     for u in users:
#         u.passwd = '******'
#     return dict(page=p, users=users)

_RE_EMAIL = re.compile(
    r'^[a-z0-9\.\-\_]+\@[a-z0-9\-\_]+(\.[a-z0-9\-\_]+){1,4}$')
_RE_SHA1 = re.compile(r'^[0-9a-f]{40}$')


@post('/api/users')
def api_register_user(*, email, name, passwd):
    if not name or not name.strip():
        raise APIValueError('name')
    if not email or not _RE_EMAIL.match(email):
        raise APIValueError('email')
    if not passwd or not _RE_SHA1.match(passwd):
        raise APIValueError('passwd')
    users = yield from User.find_All('email=?', [email])
    if len(users) > 0:
        raise APIError('register:failed', 'email', 'Email is already in use.')
    uid = next_id()
    sha1_passwd = '%s:%s' % (uid, passwd)
    user = User(id=uid, name=name.strip(), email=email, passwd=hashlib.sha1(sha1_passwd.encode('utf-8')).hexdigest(),
                image='http://www.gravatar.com/avatar/%s?d=mm&s=120' % hashlib.md5(email.encode('utf-8')).hexdigest(), admin=True)
    yield from user.save()
    # make session cookie:
    r = web.Response()
    r.set_cookie(COOKIE_NAME, user2cookie(
        user, 86400), max_age=86400, httponly=True)
    user.passwd = '******'
    r.content_type = 'application/json'
    r.body = json.dumps(user, ensure_ascii=False).encode('utf-8')
    return r


@post('/api/authenticate')
def authenticate(*, email, passwd):
    if not email:
        raise APIValueError('email', 'Invalid email.')
    if not passwd:
        raise APIValueError('passwd', 'Invalid password.')
    users = yield from User.find_All('email=?', [email])
    if len(users) == 0:
        raise APIValueError('email', 'Email not exist.')
    user = users[0]
    # check passwd:
    sha1 = hashlib.sha1()
    sha1.update(user.id.encode('utf-8'))
    sha1.update(b':')
    sha1.update(passwd.encode('utf-8'))
    if user.passwd != sha1.hexdigest():
        raise APIValueError('passwd', 'Invalid password.')
    # authenticate ok, set cookie:
    r = web.Response()
    r.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age=86400, httponly=True)
    user.passwd = '******'
    r.content_type = 'application/json'
    r.body = json.dumps(user, ensure_ascii=False).encode('utf-8')
    return r
