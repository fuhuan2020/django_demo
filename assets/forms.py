#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 19/8/6 下午4:01
# @Author  : liaozz
# @File    : forms.py

"""
    自我介绍一下
"""
from django import forms
from captcha.fields import CaptchaField
class UserForm(forms.Form):
    captcha = CaptchaField(label='验证码')
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': "Username", 'autofocus': ''}))
    password = forms.CharField(label="密码", max_length=256,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "Password"}))
class UserRegForm(forms.Form):
    captcha = CaptchaField(label='验证码')
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': "Username", 'autofocus': ''}))
    password = forms.CharField(label="密码", max_length=256,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "Password"}))
    password2 = forms.CharField(label="验证密码", max_length=256,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "Password"}))
    reg_code = forms.CharField(label="注册码", max_length=256,
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "Code"}))