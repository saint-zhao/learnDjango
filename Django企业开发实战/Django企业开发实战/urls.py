"""Django企业开发实战 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView  # 类视图，实现get方法

from .custom_site import custom_site
from blog.views import post_list , post_detail, PostDetailView, PostListView, CategoryView, TagView
from config.views import likes



urlpatterns = [
    url(r'^admin/', custom_site.urls),
    url(r'^super_admin/', admin.site.urls),

    #url(r'^$', post_list, name='index'),  # 首页下面采用类视图
    url(r'^$', PostListView.as_view(), name='index'),

    #url(r'^category/(?P<category_id>\d+)/$', post_list, name='category_list'),  # 分类文章列表
    url(r'^category/(?P<category_id>\d+)/$',CategoryView.as_view(), name='category_list'),

    #url(r'^tag/(?P<tag_id>\d+)/$', post_list, name='tab_list'),  # 标签文章列表
    url(r'^tag/(?P<tag_id>\d+)/$', TagView.as_view(), name='tab_list'),

    # url(r'^post/(?P<post_id>\d+).html$',post_detail, name='post_detail'),  #文章内容,下面使用类视图实现
    url(r'^post/(?P<post_id>\d+).html$',PostDetailView.as_view(), name='post_detail'),  #文章内容

    url(r'^likes/$', likes, name='likes'),
]
