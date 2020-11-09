from django.shortcuts import render, redirect
from django.http import HttpResponse
from login import models
from django.core.exceptions import ObjectDoesNotExist
from login import forms

# Create your views here.
"""
    登录模块
"""


def index(request):
    # 当session中无用户信息时，返回到登录界面
    if not request.session.get('is_login', None):
        return redirect('/login/')
    return render(request, 'login/index.html')


def login(request):
    if request.session.get('is_login', None):
        return redirect("/index/")
    if request.method == "POST":
        login_form = forms.User(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get("username")
            password = login_form.cleaned_data.get("password")
            try:
                user = models.User.objects.get(name=username)
            except ObjectDoesNotExist:
                message = "用户不存在"
                login_form = forms.User()
                return render(request, 'login/login.html', locals())
            if user.password == password:
                # 使用session
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                # 不允许重复登录
                return redirect("/index/")
            else:
                login_form = forms.User()
                message = "密码错误"
                return render(request, 'login/login.html', locals())
    else:
        login_form = forms.User()
        return render(request, 'login/login.html', locals())
    return render(request, 'login/login.html')


def logout(request):
    request.session.flush()
    return redirect(login)


def register(request):
    if request.session.get('is_login', None):
        return redirect('/index/')

    if request.method == 'POST':
        register_form = forms.RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            email = register_form.cleaned_data.get('email')
            sex = register_form.cleaned_data.get('sex')

            if password1 != password2:
                message = '两次输入的密码不同！'
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:
                    message = '用户名已经存在'
                    return render(request, 'login/register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:
                    message = '该邮箱已经被注册了！'
                    return render(request, 'login/register.html', locals())

                new_user = models.User()
                new_user.name = username
                new_user.password = password1
                new_user.email = email
                new_user.sex = sex
                new_user.save()

                return redirect('/login/')
        else:
            return render(request, 'login/register.html', locals())
    register_form = forms.RegisterForm()
    return render(request, 'login/register.html', locals())
