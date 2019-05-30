from django.contrib import admin

from xadmin.layout import Fieldset, Row
from xadmin.filters import RelatedFieldListFilter
from xadmin.filters import manager
import xadmin

from .models import Link, SideBar
from Django企业开发实战.custom_site import custom_site
# Register your models here.

# 使用xadmin来控制后台，从admin复制过来
# @admin.register(Link)
@xadmin.sites.register(Link)
class LinkAdmin(object):
    list_display = ['title', 'href', 'status', 'weight', 'owner']
    form_layout = (
        Fieldset(
            '基础信息',
            Row('title', 'href'),
            Row('status', 'weight'),
            'owner'
        ),
    )
    list_filter = ('owner', 'status', 'weight', 'created_time')
    search_fields = ('title',)

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(LinkAdmin,self).save_model(request, obj, form, change)


# @admin.register(SideBar)
@xadmin.sites.register(SideBar)
class SideBarAdmin(object):
    list_display = ['title', 'status', 'content', 'created_time', 'owner']
    form_layout = (
        Fieldset(
            '基本信息',
            Row('title', 'type', 'status'),
            'owner',
        ),
        Fieldset(
            '内容信息',
            'content',
        )
    )
    list_filter = ('type', 'status', 'created_time')
    search_fields = ('title',)

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(SideBarAdmin, self).save_model(request, obj, form, change)
