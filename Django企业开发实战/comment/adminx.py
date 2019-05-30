from django.contrib import admin


from .models import Comment
from Django企业开发实战.custom_site import custom_site

# Register your models here.
# 使用xadmin来控制
import xadmin
from xadmin.layout import Fieldset, Row
from xadmin.filters import manager
from xadmin.filters import RelatedFieldListFilter

@xadmin.sites.register(Comment)
class CommentAdmin(object):
    list_display = ['target', 'nickname', 'content', 'email', 'status', 'created_time']

