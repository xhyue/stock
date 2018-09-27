from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import logout, login, authenticate
import logging
from .models import *
import json

# Create your views here.


auth_check = 'MarcelArhut'

# 登录
def login_(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        if not username:
            return HttpResponse(json.dumps({"result":False, "data":"", "error":"用户名密码不能为空", }))
        # 使用django提供的验证方法，传入用户名和密码，会返回一个user对象
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            user.backend = 'django.contrib.auth.backends.ModelBackend'  # 指定默认的登录验证方式
            login(request, user)
            return redirect(request.POST.get('source_url'))
        else:
            return HttpResponse(json.dumps({"result":False, "data":"", "error":"用户名或密码错误"}))
            # return render(request, 'login.html', {'message': "用户名或密码错误"})
    else:
        return HttpResponse(json.dumps({"result":True, "data":"", "error":""}))
        # return render(request, 'login.html')


# 注册
def register_(request):
    if request.method == 'POST':
        new_user = UserInfo()
        new_user.username = request.POST.get('username', '')
        if not new_user.username:
            return HttpResponse(json.dumps({"result":False, "data":"", "error":"用户名密码不能为空"}))
        try:
            olduser = UserInfo.objects.filter(username=new_user.username)
            if olduser:
                return HttpResponse({"result":False, "data":"", "error":"该用户名已经存在"})
                # return render(request, 'register.html', {'message': '该用户名已经存在'})
        except ObjectDoesNotExist as e:
            logging.warning(e)
        if request.POST.get('pwd') != request.POST.get('cpwd'):
            return HttpResponse({"result": False, "data": "", "error": "两次输入的密码不一致"})
            # return render(request, 'register.html', {'message': '两次输入的密码不一致'})
        new_user.password = make_password(request.POST.get('pwd'), auth_check, 'pbkdf2_sha1')
        try:
            new_user.save()
        except ObjectDoesNotExist as e:
            logging.warning(e)
        # return redirect('/')
        return HttpResponse(json.dumps({"result":True, "data":"", "error":""}))
    else:
        return HttpResponse(json.dumps({"result":True, "data":"", "error":""}))
        # return render(request, 'register.html')


# 注销
def logout_(request):
    try:
        logout(request)
    except Exception as e:
        logging.warning(e)
    return redirect('/')


# 银行卡绑定
def bank_(request, band, bandNo):
    user = UserInfo.objects.filter(id=request.user.id)
    if len(user) > 0:
        Bank.objects.create(user=user[0].id, band=band, bandNo=bandNo)
    else:
        return HttpResponse(json.dumps({"result": False, "data": "", "error": "去登录"}))