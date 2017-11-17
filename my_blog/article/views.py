# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from article import models
from django.views.decorators.csrf import csrf_protect


# Create your views here.

# 第一个参数必须是 request，与网页发来的请求有关，request 变量里面包含get或post的内容，用户浏览器，系统等信息在里面
def home(request):
    string = 'a,b,cd'
    tutorialList = ["HTML", "CSS", "jQuery", "Python", "Django"]
    info_dict = {'site': u'自强学堂', 'content': u'各种IT技术教程'}
    List = map(str, range(100))
    return render(request, 'home.html', {'TutorialList': tutorialList,
                                         'List': List})  # render 是渲染模板,使用render的时候，Django 会自动找到 INSTALLED_APPS 中列出的各个 app 下的 templates 中的文件


def add(request):
    a = request.GET.get('a', 0)
    b = request.GET.get('b', 0)
    # 当请求地址的时候没有加a和b的值的时候，这样写的话a和b的值就是默认为0
    c = int(a) + int(b)
    return HttpResponse(str(c))


def add2(request, a, b):
    c = int(a) + int(b)
    return HttpResponse(str(c))


def old_add2_redirect(request, a, b):
    return HttpResponseRedirect(
        reverse('add2', args=(a, b))
    )


# 注册账户
@csrf_protect
def addDate(request):
    if request.method == 'POST':
        u_name = request.POST['username']
        u_passw = request.POST['password']
        u_email = request.POST['email']
        models.Userinf.objects.create(username=u_name, password=u_passw, email=u_email)
    return HttpResponse("register success")

# 更改密码
