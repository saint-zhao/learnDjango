from django.contrib.auth.models import User
from django.template.loader import render_to_string  #


from django.db import models


# Create your models here.


class Link(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )

    title = models.CharField(max_length=128, verbose_name='标题')
    href = models.URLField(verbose_name='网站地址')
    status = models.IntegerField(choices=STATUS_ITEMS, verbose_name='状态')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    weight = models.PositiveIntegerField(default=1, choices=zip(range(1, 6), range(1, 6)),
                                         verbose_name='权重', help_text='权重高表示排在前面')
    owner = models.ForeignKey(User, verbose_name='作者')

    class Meta:
        verbose_name = verbose_name_plural = '友链'

    def __str__(self):
        return '{}'.format(self.title)


class SideBar(models.Model):
    STATUS_SHOW = 1
    STATUS_HIDE = 0
    STATUS_ITEMS = (
        (STATUS_SHOW, '展示'),
        (STATUS_HIDE, '隐藏'),
    )

    DISPALY_HTML = 1
    DISPALY_LATEST = 2
    DISPALY_HOT = 3
    DISPALY_COMMENT = 4

    SIDE_TYPE = (
        (DISPALY_HTML, 'HTML'),
        (DISPALY_LATEST, '最新文章'),
        (DISPALY_HOT, '最热文章'),
        (DISPALY_COMMENT, '最近评论'),
    )

    title = models.CharField(max_length=255, verbose_name='标题')
    type = models.IntegerField(choices=SIDE_TYPE, verbose_name='展示类型')
    status = models.IntegerField(choices=STATUS_ITEMS, verbose_name='状态')
    content = models.CharField(max_length=500, verbose_name='内容', blank=True, help_text='如果不是HTML类型可为空')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    owner = models.ForeignKey(User, verbose_name='作者')

    class Meta:
        verbose_name = verbose_name_plural = '侧边栏'

    def __str__(self):
        return '{}'.format(self.title)

    @classmethod
    def get_all(cls):
        return cls.objects.filter(status=cls.STATUS_SHOW)

    def content_html(self):
        """直接渲染模板"""
        from blog.models import Post
        from comment.models import Comment

        result = ''
        if self.type == self.DISPALY_HTML:
            result = self.content

        elif self.type == self.DISPALY_LATEST:
            context = {
                'posts': Post.latest_posts(with_related=False)
            }
            result = render_to_string('config/blocks/sidebar_posts.html',context)

        elif self.type == self.DISPALY_HOT:
            context = {
                'posts':Post.hot_posts()
            }
            result = render_to_string('config/blocks/sidebar_posts.html',context)

        elif self.type == self.DISPALY_COMMENT:
            context = {
                'comments':Comment.objects.filter(status=Comment.STATUS_NORMAL)
            }
            #print(context,1111)
            result = render_to_string('config/blocks/sidebar_comments.html',context)
        return result
