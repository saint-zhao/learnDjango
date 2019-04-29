from django.contrib import admin

from .models import Link, SideBar
from Django企业开发实战.custom_site import custom_site
# Register your models here.


# @admin.register(Link)
@admin.register(Link, site=custom_site)
class LinkAdmin(admin.ModelAdmin):
    list_display = ['title', 'href', 'status', 'weight', 'owner']
    fields = (
        ('title', 'href',),
        ('status', 'weight'),
        'owner'
    )
    list_filter = ('owner', 'status', 'weight', 'created_time')
    search_fields = ('title',)

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(LinkAdmin,self).save_model(request, obj, form, change)


# @admin.register(SideBar)
@admin.register(SideBar, site=custom_site)
class SideBarAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'content', 'created_time', 'owner']
    fields = (
        ('title', 'type', 'status'),
        'owner',
        'content',
    )
    list_filter = ('type', 'status', 'created_time')
    search_fields = ('title',)

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(SideBarAdmin, self).save_model(request, obj, form, change)
