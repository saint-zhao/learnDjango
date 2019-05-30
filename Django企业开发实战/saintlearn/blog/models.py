from django.contrib.auth.models import User  # 使用Django自导的用户模型
from django.utils.functional import cached_property

import mistune

from django.db import models
from django.db.models import Q


# Create your models here.


class Category(models.Model):
    """这是分类的模型"""
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )

    name = models.CharField(max_length=128, verbose_name='名称')
    status = models.IntegerField(choices=STATUS_ITEMS, verbose_name='状态')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    is_nav = models.BooleanField(default=False, verbose_name='是否为导航')
    owner = models.ForeignKey(User, verbose_name='作者', related_name='category_owner')

    class Meta:
        verbose_name = verbose_name_plural = '分类'

    def __str__(self):
        return '分类:{}'.format(self.name)

    @classmethod
    def get_nav(cls):
        "这个用来获取是否为导航的分类"
        categories = cls.objects.filter(status=cls.STATUS_NORMAL)
        nav_categores = []
        norman_categories = []
        for categorie in categories:
            if categorie.is_nav:
                nav_categores.append(categorie)
            else:
                norman_categories.append(categorie)
        return {
            'navs':nav_categores,
            'categories':norman_categories
        }


class Tag(models.Model):
    """这是标签的模型"""
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )

    name = models.CharField(verbose_name='名字', max_length=255)
    status = models.IntegerField(choices=STATUS_ITEMS, verbose_name='状态')
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    owner = models.ForeignKey(User, verbose_name='作者')

    class Meta:
        verbose_name = verbose_name_plural = '标签'

    def __str__(self):
        return '标签：{}'.format(self.name)


class Post(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_DRAFT = 2
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
        (STATUS_DRAFT, '草稿'),
    )
    pv = models.PositiveIntegerField(default=1)
    uv = models.PositiveIntegerField(default=1)  # 统计每篇文章的访问量

    title = models.CharField(verbose_name='标题', max_length=120)
    description = models.CharField(verbose_name='概述', blank=True, max_length=500)
    content = models.TextField(verbose_name='内容', help_text='正文必须为Markdown格式')
    context_html = models.TextField(verbose_name='正文html代码', blank=True, editable=False)
    status = models.IntegerField(choices=STATUS_ITEMS, verbose_name='状态')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    owner = models.ForeignKey(User, verbose_name='作者')
    category = models.ForeignKey(Category, verbose_name='分类',)
    tag = models.ManyToManyField(Tag, verbose_name='标签',related_name='tag_post')
    is_md = models.BooleanField(default=False, verbose_name='markdown语法') # 这个字段用来判断用哪个编编辑器

    class Meta:
        verbose_name = '文章'
        ordering = ['-id']
        # 根据id进行降序排序

    def __str__(self):
        return '{}'.format(self.title)

    @staticmethod
    def get_by_tag(tag_id):
        "这个方法用来获取标签，以及标签下所有的post对象"
        try:
            tag = Tag.objects.get(id=tag_id)
        except tag.DoesNotExist:
            tag = None
            post_list = []
        else:
            post_list = Tag.tag_post.filter(status=Post.STATUS_NORMAL).select_related('owner', 'category')

        return post_list, tag

    @staticmethod
    def get_by_category(category_id):
        "这个方法用来获取分类，以及分类下所有的post对象"
        try:
            category = Category.objects.get(id=category_id)
        except category.DoesNotExist:
            category = None
            post_list = []
        else:
            post_list = category.post_set.filter(status=Post.STATUS_NORMAL).select_related('owner', 'category')

        return post_list, category

    @classmethod
    def latest_posts(cls, with_related=True):
        "这个方法用来获取所有的状态为正常的post对象"
        queryset = cls.objects.filter(status=cls.STATUS_NORMAL).prefetch_related('tag')
        if with_related:
            queryset = queryset.select_related('owner', 'category')
        return queryset

    @classmethod
    def hot_posts(cls):
        return cls.objects.filter(status=cls.STATUS_NORMAL).order_by('-pv')

    def save(self, *args, **kwargs):
        if self.is_md:
            self.context_html = mistune.markdown(self.content)
        else:
            self.context_html = self.content
        super().save(*args, **kwargs)

    @cached_property  # 这份装饰器其的作用是把我们返回的数据捆绑到实例上
    def tags(self):
        """获得所有标签的方法"""
        return ''.join(self.tag.values_list('name', flat=True))




