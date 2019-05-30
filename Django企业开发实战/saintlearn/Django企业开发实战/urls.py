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
from django.contrib.sitemaps import views as sitrmap_views # 实现RSS和Sitemap的方法

import xadmin
from .autocomplete import CategoryAutocomplete, TagAutocomplete

#配置ckeditor接收文件的接口
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static

from blog.views import (PostDetailView, PostListView, CategoryView, TagView, SearchView, AutherVier)
from config.views import LikeView
from comment.views import CommentView
from blog.sitemap import PostSitemap
from blog.rss import LatestPostFeed
from blog.apis import PostList, post_list


urlpatterns = [
    url(r'^admin/', xadmin.site.urls, name='xadmin'),
    url(r'^super_admin/', admin.site.urls),

    #url(r'^$', post_list, name='index'),  # 首页下面采用类视图
    url(r'^$', PostListView.as_view(), name='index'),

    #url(r'^category/(?P<category_id>\d+)/$', post_list, name='category_list'),  # 分类文章列表
    url(r'^category/(?P<category_id>\d+)/$',CategoryView.as_view(), name='category_list'),

    #url(r'^tag/(?P<tag_id>\d+)/$', post_list, name='tab_list'),  # 标签文章列表
    url(r'^tag/(?P<tag_id>\d+)/$', TagView.as_view(), name='tab_list'),

    url(r'^search/$', SearchView.as_view(), name='search'),  #显示搜索页面的url

    url(r'^author/(?P<author_id>\d+)/$',AutherVier.as_view(), name='author_list'),  # 显示作者的所有文章

    # url(r'^post/(?P<post_id>\d+).html$',post_detail, name='post_detail'),  #文章内容,下面使用类视图实现
    url(r'^post/(?P<post_id>\d+).html$',PostDetailView.as_view(), name='post_detail'),  #文章内容

    #url(r'^likes/$', likes, name='likes'),
    url(r'^likes/$',LikeView.as_view(),name='likes'),  # 显示所有友链的列表

    url(r'^comment/$', CommentView.as_view(), name='comment'),

    url(r'^rss|feed/', LatestPostFeed(), name='rss'),

    url(r'^sitemap\.xml$', sitrmap_views.sitemap, {'sitemaps': {
        'posts': PostSitemap}}),

    url(r'^category-autocomplete/$', CategoryAutocomplete.as_view(), name='category-autocomplete'),
    url(r'^tag-autocomplete/$', TagAutocomplete.as_view(), name='tag-autocomplete'), #这两个url是自动补全插件

    # 配置ckeditor插件上传文件接收文件的接口
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),

    # 使用djangoRestFarmwork插件的url
    url(r'^api/post/', post_list, name='post-list'),
    #url(r'^api/post/', PostList.as_view(), name='post-list'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    print('1111111')
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
