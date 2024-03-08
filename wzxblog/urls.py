from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    # 用户注册的路由url
    path("registe/", views.registe, name='registe'),

    path("login/", views.login, name='login'),

    path("logout/", views.logout, name='logout'),
    path("", views.indexview.as_view(), name='index'),]
