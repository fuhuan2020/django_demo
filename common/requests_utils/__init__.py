#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 20/8/21 下午3:57
# @Author  : liaozz
# @File    : __init__.py.py

"""
    自我介绍一下
"""
def request_method(request,func_post=None,func_post_js=None,func_get=None,*args,**kwargs):
    '''
    封装区分不通请求方式

    :param request:
    :param func_post:  表单post请求
    :param func_post_js: js post请求
    :param func_get: get 请求
    :param args:
    :param kwargs:
    :return:
    '''

    def form_post(request,*args,**kwargs):
        pass
    def js_post(request,*args,**kwargs):
        '''
        必须请求参数中必须有js键
        '''
        pass
    def get(request,*args,**kwargs):
        pass

    if request.method == 'POST':
        request_dir = request.POST
        js = request_dir.get("js")
        if js:
            if not func_post_js:
                raise ValueError("raise", "func_post_form is None")
            return func_post_js(request,*args,**kwargs)
        else:
            if not func_post:
                raise ValueError("raise", "func_post_js is None")
            return func_post(request,*args,**kwargs)
    else:
        if not func_get:
            raise ValueError("raise", "func_get is None")
        return func_get(request,*args,**kwargs)

if __name__ == "__main__":
    pass