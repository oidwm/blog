
from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.views.generic import ListView

from . import forms
from . import models


class indexview(ListView):
    """
    首页view 方法
    :param request:
    :return:
    """
    model = models.Bloginfo
    template_name = 'blog/index.html'
    context_object_name = 'blog_list'


def registe(request):
    """
    用户注册view 方法
    :param request:
    :return:
    """
    if request.method == 'POST':
        form_obj = forms.reg_form(request.POST, request.FILES)
        if form_obj.is_valid():
            # 确认密码这个字段
            form_obj.cleaned_data.pop('repassword')

            user_obj = models.Reguser.objects.create_user(**form_obj.cleaned_data, is_staff=1, is_superuser=1)

            # 联动完成登录动作
            auth.login(request, user_obj)

            # 跳转到首页
            return redirect("/")
        else:
            return render(request, "blog/registe.html", {'formobj': form_obj})
    else:
        form_obj = forms.reg_form()
        return render(request, "blog/registe.html", {'formobj': form_obj})


def login(request):
    """
    用户登录view 方法
    :param request:
    :return:
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_obj = auth.authenticate(username=username, password=password)
        if user_obj:
            auth.login(request, user_obj)
            return redirect('/')
        else:
            return render(request, 'blog/login.html', {'error': '用户名或密码错误.'})
    else:
        return render(request, 'blog/login.html')


def logout(request):
    """
    用户退出view 方法
    :param request:
    :return:
    """
    auth.logout(request)
    return redirect('/')
