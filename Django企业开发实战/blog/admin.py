from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.contrib.admin.models import LogEntry, CHANGE   # 这是内置的日志模块

from .models import Post, Tag, Category
from .adminforms import PostAdminForm
from Django企业开发实战.custom_site import custom_site
from Django企业开发实战.base_admin import BaseOwnerAdmin


# Register your models here.



class PostInline(admin.TabularInline): # 样式不一样
    """这个雷是为了实现在分类页面可以直接编辑文章"""
    fields = ['title', 'description']
    extra = 1 # 额外控制几个
    model = Post


class CategiryOwnerFilter(admin.SimpleListFilter):
    """自定义过滤器，只展示当前用户的分类"""
    title = '用户分类过滤器'
    parameter_name = 'owner_category'

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id', 'name')

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset


@admin.register(LogEntry,site=custom_site)
class LogEntryAdmin(admin.ModelAdmin):
    """这是在页面注册日至"""
    list_display = ['object_repr', 'object_id', 'action_flag', 'user', 'change_message']

# @admin.register(Category) 这是使用默认的site，下面的是使用定制的site
@admin.register(Category, site=custom_site)
class CatrgoryAdmin(BaseOwnerAdmin):
    """这个类是分类管理的模型"""
    list_display = ('name', 'owner', 'status', 'is_nav', 'created_time')
    fields = ('name', 'status', 'is_nav')
    inlines= [PostInline, ]

    # 下面这一块已经愁渠道基类里埋年去了，继承之后就不需要重复写了
    # def save_model(self, request, obj, form, change):
    #     obj.owner = request.user
    #     return super(CatrgoryAdmin, self).save_model(request, obj, form, change)
    #
    # def get_queryset(self, request):
    #     qs = super(CatrgoryAdmin, self).get_queryset(request)
    #     return qs.filter(owner=request.user)


# @admin.register(Tag)
@admin.register(Tag, site=custom_site)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'status', 'created')
    fields = ('name', 'status', 'owner')

    def save_model(self, request, obj, form, change):
        # 自定义保存方法
        obj.owner = request.user
        return super(TagAdmin, self).save_model(request, obj, form, change)


# @admin.register(Post)
@admin.register(Post, site=custom_site)
class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForm
    # 这个是自定义表单，
    list_display = ('title', '' 'owner', 'category', 'status', 'created_time', 'operator')
    list_display_links = []
    list_filter = [CategiryOwnerFilter, 'created_time', 'owner']
    search_fields = ['title', 'category__name']

    actions_on_top = True
    actions_on_bottom = True

    # 编辑页面
    save_on_top = True
    exclude = ('owner',)
    fields = (
        ('title', 'category'),
        'description',
        'status',
        'content',
        'tag',
    )

    def operator(self, obj):
        return format_html(
            "<a href='{}'>编辑</a>",
            reverse('cust_admin:blog_post_change', args=(obj.id,))
        )

    operator.short_description = '操作'

    # 下面这一块已经愁渠道基类里埋年去了，继承之后就不需要重复写了
    # def save_model(self, request, obj, form, change):
    #     obj.owner = request.user
    #     return super(PostAdmin, self).save_model(request, obj, form, change)
    #
    # def get_queryset(self, request):
    #     qs = super(PostAdmin, self).get_queryset(request)
    #     return qs.filter(owner=request.user)