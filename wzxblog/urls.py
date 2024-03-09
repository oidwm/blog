from django.urls import path, re_path
from . import views

app_name = 'blog'
urlpatterns = [
    # 用户注册的路由url
    path("registe/", views.registe, name='registe'),

    path("login/", views.login, name='login'),

    path("logout/", views.logout, name='logout'),

    path("", views.indexview.as_view(), name='index'),

    re_path("archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$", views.archives.as_view(), name='archives'),

    re_path('category/(?P<categoryid>[0-9]+)/$', views.categoryview, name='category'),

    re_path("tag/(?P<tagid>[0-9]+)/$", views.tagview.as_view(), name='tag'),

    path("author/<int:userid>/", views.authorview.as_view(), name='author'),
]
