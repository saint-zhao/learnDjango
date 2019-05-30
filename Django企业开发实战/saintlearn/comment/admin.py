from django.contrib import admin


from .models import Comment
from Django企业开发实战.custom_site import custom_site

# Register your models here.


# @admin.register(Comment)下面使用自定义的site
@admin.register(Comment,site=custom_site)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['target','nickname','content','email','status','created_time']

