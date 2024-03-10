from django.contrib import auth
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404, render
from .models import Bloginfo, Category, Tag

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


class tagview(ListView):
    model = models.Bloginfo
    template_name = 'blog/tag.html'
    context_object_name = 'blog_list'

    def get_queryset(self):
        tag_id = self.kwargs.get('tagid')
        tag = get_object_or_404(models.Tag, pk=tag_id)
        return super(tagview, self).get_queryset().filter(tags=tag).order_by('-create_time')

    def get_context_data(self, **kwargs):
        context = super(tagview, self).get_context_data(**kwargs)
        context['tag'] = get_object_or_404(models.Tag, pk=self.kwargs.get('tagid'))
        return context


class authorview(ListView):
    model = models.Bloginfo
    template_name = 'blog/author.html'
    context_object_name = 'blog_list'

    def get_queryset(self):
        author = get_object_or_404(models.Reguser, pk=self.kwargs.get('userid'))
        return super(authorview, self).get_queryset().filter(author=author).order_by('-create_time')

    def get_context_data(self, **kwargs):
        context = super(authorview, self).get_context_data()
        context['author'] = get_object_or_404(models.Reguser, pk=self.kwargs.get('userid'))
        return context


class archives(ListView):
    """
    首页view 方法
    :param request:
    :return:
    """
    model = models.Bloginfo
    template_name = 'blog/archives.html'
    context_object_name = 'blog_list'

    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(archives, self).get_queryset().filter(create_time__year=year, create_time__month=month).order_by(
            '-create_time')

class blogdatailview(DetailView):
    model = models.Bloginfo
    template_name = 'blog/blog_detail.html'
    context_object_name = 'blog'
    pk_url_kwarg = 'blogid'

    def get_object(self, queryset=None):
        blog = super(blogdatailview, self).get_object(queryset=None)
        blog.add_one_views()
        return blog



def registe(request):
    """
    用户注册view 方法
    :param request:
    :return:
    """
    # 如果请求方法是POST
    if request.method == 'POST':
        # 实例化注册表单
        form_obj = forms.reg_form(request.POST, request.FILES)
        # 如果表单验证通过
        if form_obj.is_valid():
            # 确认密码这个字段
            form_obj.cleaned_data.pop('repassword')

            # 创建用户
            user_obj = models.Reguser.objects.create_user(**form_obj.cleaned_data, is_staff=1, is_superuser=1)

            # 联动完成登录动作
            auth.login(request, user_obj)

            # 跳转到首页
            return redirect("/")
        else:
            # 如果表单验证不通过，返回注册页面，并把错误信息传到页面
            return render(request, "blog/registe.html", {'formobj': form_obj})
    else:
        # 如果请求方法是GET，实例化注册表单
        form_obj = forms.reg_form()
        # 返回注册页面，并把表单传到页面
        return render(request, "blog/registe.html", {'formobj': form_obj})


def login(request):
    """
    用户登录view 方法
    :param request:
    :return:
    """
    if request.method == 'POST':  # 如果请求方法是POST
        username = request.POST.get('username')  # 获取POST请求中的username参数
        password = request.POST.get('password')  # 获取POST请求中的password参数
        user_obj = auth.authenticate(username=username, password=password)  # 通过用户名和密码获取用户对象
        if user_obj:  # 如果用户对象存在
            auth.login(request, user_obj)  # 登录
            return redirect("/")
        else:
            return render(request, 'blog/login.html', {'error': '用户名或密码错误.'})  # 返回登录页面，并传递错误信息
    else:
        return render(request, 'blog/login.html')  # 如果请求方法不是POST，则返回登录页面


def categoryview(request, categoryid):
    # 获取分类对象
    category = get_object_or_404(Category, pk=categoryid)

    # 获取属于该分类的博客文章列表
    blog_list = Bloginfo.objects.filter(category=category).order_by('-create_time')

    # 渲染模板并传递上下文
    context = {
        'blog_list': blog_list,
        'category': category,
    }
    return render(request, 'blog/category.html', context)


def logout(request):
    """
    用户退出view 方法
    :param request:
    :return:
    """
    auth.logout(request)
    return redirect('/')
