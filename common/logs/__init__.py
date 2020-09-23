#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 20/8/21 上午9:53
# @Author  : liaozz
# @File    : __init__.py.py

from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import  HttpResponse
import logging,functools,traceback,json

"""
    自我介绍一下
"""

def request_log(func):
    '''
    打印request请求参数日志
    :param func:
    :return:
    '''
    def print_request(result=None,*args, **kwargs):
        def print_request_log(result,ar):
            if result:
                if isinstance(result,HttpResponse):
                    result=result.content
            if isinstance(ar, WSGIRequest):
                if ar.method == "POST":
                    logging.info(dict(post=ar.POST,result=result))
                elif ar.method == "GET":
                    logging.info(dict(post=ar,result=result))
        if args:
           for ar in args:
               print_request_log(result,ar)

        if kwargs:
            keys=kwargs.keys()
            for key in keys:
                ar=kwargs[key]
                print_request_log(result,ar)

    @functools.wraps(func)
    def dd(*args, **kwargs):
        result=func(*args, **kwargs)
        try:
            print_request(result,*args, **kwargs)
        except Exception as e:
            tr = traceback.format_exc()
            logging.info(tr)
        return result
    return dd
if __name__ == "__main__":
    pass