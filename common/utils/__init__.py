#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 20/8/20 上午10:20
# @Author  : liaozz
# @File    : __init__.py.py

import time,datetime,json,hashlib,base64,re,hmac,os,traceback
from hashlib import sha1

def formate_time(formate="%Y-%m-%d %H:%M:%S"):
    return time.strftime(formate)


def formate_datetime(date_string, cls="%Y-%m-%d %H:%M:%S"):
    d = datetime.datetime.strptime(date_string, cls)
    t = d.timetuple()
    return int(time.mktime(t))

def get_json_md5_base64_sign(datastr, key):
    args1 = json.dumps(datastr, separators=(',', ':'))
    key_data = args1 + key  # 添加密钥进行加密
    m = hashlib.md5()  # md5加密
    m.update(key_data.encode(encoding="utf8"))
    psw = m.hexdigest()
    args2 = base64.b64encode(psw.encode(encoding="utf8"))  # base64加密
    return args2.decode()

def checkip(ip):
    '''
    判断是否为ip
    :param ip:
    :return:
    '''
    p = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    if p.match(ip):
        return True
    else:
        return False
def mkdirs(paths):
    '''
    :param paths: 路径，或者list
    :return:
    '''
    def checkout(path):
        path_array = path.split("/")
        path_str = ""
        for p in path_array:
            if not "." in p:
                path_str = path_str + "/" + p
                if not os.path.exists(path_str):
                    os.mkdir(path_str)
    if isinstance(paths,list):
        for path in paths:
            checkout(path)
    elif isinstance(paths,str):
        checkout(paths)
def open_write_json(file_path,data_dict):
    '''
    保存json文件
    :param file_path: 文件路径
    :param data_dict:  字典
    :return:
    '''
    try:
        with open(file_path, "w") as kvm_info:
            json.dump(data_dict, kvm_info, indent=4, ensure_ascii=False)
    except Exception as e:
        traceback.print_exc()
        return False
    return True

def open_read_json(file_path):
    '''
    读取文件
    :param file_path:
    :return:
    '''
    kvm_info_dict=""
    if os.path.exists(file_path):
        try:
            with open(file_path, "r") as kvm_info:
                kvm_info_dict = json.load(kvm_info)
        except Exception as e:
            traceback.print_exc()
            pass
    return kvm_info_dict

if __name__ == "__main__":
    pass