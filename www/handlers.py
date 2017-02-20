#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2017-02-18 19:05:40
# @Author  : Han Zhiyun (hanzhiyun1995@qq.com)

import time
from coroweb import get, post
from aiohttp import web
from models import User, Comment, Blog, next_id


@get('/blog')
async def handler_url_blog(request):
    body='<h1>Awesome: /blog</h1>'
    return body

@get('/greeting')
async def handler_url_greeting(*,name,request):
    body='<h1>Awesome: /greeting %s</h1>'%name
    return body

@get('/input')
async def handler_url_input(request):
    body='<form action="/result" method="post">E-mail: <input type="email" name="user_email" /><input type="submit" /></form>'
    return body

@post('/result')
async def handler_url_result(*,user_email,request):
    body='<h1>您输入的邮箱是%s</h1>'%user_email
    return body

@get('/index')
async def handler_url_index(request):
    body='<h1>Awesome: /index</h1>'
    return body

@get('/create_comment')
async def handler_url_create_comment(request):
    body='<h1>Awesome: /create_comment</h1>'
    return body
'''
@get('/')
async def index(request):
    users = await User.findAll()
    return {
        '__template__': 'test.html',
        'users': users
    }
'''
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
        'blogs': blogs
    }

