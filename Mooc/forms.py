# -*- coding:utf-8 -*-
__author__ = 'yanhaoran'
from django import forms
from django.contrib.auth.models import User
from django.contrib import auth

class LoginForm(forms.Form):
    username = forms.CharField(label=u'用户名/邮箱', widget=forms.TextInput, max_length=20)
    password = forms.CharField(label=u'密码', widget=forms.PasswordInput, max_length=20)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username is None:
            raise forms.ValidationError(u'用户名不能为空')
        elif len(username) <= 5:
            raise forms.ValidationError(u'长度不能小于6')
        # 中间还有很多elif...
        else:
            filterResults = User.objects.filter(username=username)
            if len(filterResults) == 0:
                raise forms.ValidationError(u'用户名不存在')
        return username

    def clean_password(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if password is None:
            raise forms.ValidationError(u'密码不能为空')
        else:
            filterResults = User.objects.filter(username=username)
            if len(filterResults) == 1:
                user = auth.authenticate(username=username, password=password)
                if user is None:
                    raise forms.ValidationError(u'密码不正确')

        return password

class RegisterForm(forms.Form):
    username = forms.EmailField(label=u'邮箱', max_length=20)
    password1 = forms.CharField(label=u'密码', widget=forms.PasswordInput, max_length=20)
    password2 = forms.CharField(label=u'密码', widget=forms.PasswordInput, max_length=20)
    nickname = forms.CharField(label=u'昵称', max_length=20)
    # school = forms.CharField(label=u'学校', max_length=20, required=False)
    # birthday = forms.DateField(label=u'生日', widget=forms.DateInput(format = '%d/%m/%Y'))
    # sex = forms.ChoiceField(label=u'性别', choices=(('M', u'男'), ('F', u'女')))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        #判断用户名是否为空
        if username is None:
            raise forms.ValidationError(u'邮箱不能为空')
        else:
            filterResults = User.objects.filter(username=username)
            #用户是否被注册
            if len(filterResults) != 0:
                raise forms.ValidationError(u'此邮箱已被注册')
            return username

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        #两次密码不一致
        if  password1 != password2:
            raise forms.ValidationError(u'两次密码不一致')
        #密码长度必须为6-16个字符
        elif len(password1) > 16 or len(password1) < 6  :
            raise forms.ValidationError(u'密码长度必须为6-16个字符')
        #密码不能包含空格
        else :
            str1 = ''.join(password1.split())
            if( len(password1)  !=  len(str1) ):
                raise forms.ValidationError(u'密码不能包含空格')
        return password2


