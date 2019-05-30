from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from xadmin.layout import Row, Fieldset, Container
from xadmin.filters import manager  # 这两个导入时引入xadmin的过滤器
from xadmin.filters import RelatedFieldListFilter
import xadmin

from .models import Post, Tag, Category
from .adminforms import PostAdminForm
from Django企业开发实战.custom_site import custom_site
from Django企业开发实战.base_adminx import BaseOwnerAdmin

# 使用admin 复制过来使用xadmin插件来控制
# Register your models here.



class PostInline():
    """这个雷是为了实现在分类页面可以直接编辑文章"""
    form_layout = Fieldset(
        Container(
            Row('title', 'category')
        )
    )
    extra = 1 # 额外控制几个
    model = Post


class CategoryOwnerFilter(RelatedFieldListFilter):
    """自定义过滤器，只展示当前用户的分类,使用xadmin的方式"""
    @classmethod
    def test(cls, field, request, params, model, admin_view, field_path):
        return field.name == 'category'

    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin, field_path)
        # 重新获取lookup_choices，根据owner过滤
        self.lookup_choices = Category.objects.filter(owner=request.user).values_list('id', 'name')

manager.register(CategoryOwnerFilter, take_priority=True)

@xadmin.sites.register(Category)
class CatrgoryAdmin(BaseOwnerAdmin):
    """这个类是分类管理的模型"""
    list_display = ('name', 'owner', 'status', 'is_nav', 'created_time')
    fields = ('name', 'status', 'is_nav')
    inlines= [PostInline, ]

@xadmin.sites.register(Tag)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'owner', 'status', 'created')
    fields = ('name', 'status', 'owner')

    def save_models(self):
        # 自定义保存方法
        self.new_obj.owner = self.request.user
        return super(TagAdmin, self).save_models()

@xadmin.sites.register(Post)
class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForm
    # 这个是自定义表单，
    list_display = ('title', 'owner', 'category', 'status', 'created_time', 'operator')
    list_display_links = []
    list_filter = ['category', 'created_time', 'owner']
    search_fields = ['title', 'category__name']

    actions_on_top = True
    actions_on_bottom = True

    # 编辑页面
    save_on_top = True
    exclude = ('owner',)

    form_layout = (
        Fieldset(
            '基础信息',
            Row('title', 'category'),
            'status',
            'tag',
        ),
        Fieldset(
            '内容信息',
            'description',
            'is_md',
            'content_ck',
            'content_md',
            'content',
        )
    )# 上面这个字段是配置xadmin的布局

    def operator(self, obj):
        return format_html(
            "<a href='{}'>编辑</a>",
            self.model_admin_url('change', obj.id)
        )

    operator.short_description = '操作'
