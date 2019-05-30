"""这是个人定制的admin site"""
from django.contrib.admin import AdminSite


class CustomSite(AdminSite):
    site_header = 'Django企业开发实战'
    site_title = 'Django企业开发实战管理后台'
    index_title = '首页'

custom_site = CustomSite(name='cust_admin')
