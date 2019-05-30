# coding:utf-8

# 这个文件是为了实现rss输出的模块

from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.utils.feedgenerator import Rss201rev2Feed


from .models import Post

class ExtendedRSSFeed(Rss201rev2Feed):
    def add_item_elements(self, handler, item):
        super(ExtendedRSSFeed,self).add_item_elements(handler, item)
        handler.addQuickElement('content:html', item['content_html'])

class LatestPostFeed(Feed):
    feed_type = ExtendedRSSFeed
    title = "saint 博客系统"
    link = '/rss/'
    description = '这个博客系统基于Django开发'

    def items(self):
        return Post.objects.filter(status=Post.STATUS_NORMAL)[:5]    # 模板默认按id排序

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

    def item_link(self, item):
        return reverse('post_detail', args=[item.pk])

    def item_extra_kwargs(self, item):
        return {'content_html': self.item_content_html(item)}

    def item_content_html(self, item):
        return item.context_html
