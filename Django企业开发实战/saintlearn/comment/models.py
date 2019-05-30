from django.contrib.auth.models import User

from django.db import models

from blog.models import Post

# Create your models here.

class Comment(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )

    nickname = models.CharField(max_length=128, verbose_name='呢称')
    target = models.CharField(max_length=255, verbose_name='评论对象')
    content = models.CharField(max_length=500, verbose_name='评论内容')
    website = models.URLField(verbose_name='网站')
    email = models.EmailField(verbose_name='邮箱')
    status = models.IntegerField(choices=STATUS_ITEMS, default=STATUS_NORMAL, verbose_name='状态')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = verbose_name_plural = '评论'

    def __str__(self):
        return '{}'.format(self.content)

    @classmethod
    def get_by_target(cls, target):
        return cls.objects.filter(target=target, status=cls.STATUS_NORMAL)
