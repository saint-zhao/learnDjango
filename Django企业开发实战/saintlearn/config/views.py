from django.shortcuts import render
from django.views.generic import ListView, TemplateView

from blog.views import CommonViewMixin
from .models import Link

# Create your views here.

def likes(request):
    "这是显示外部链接的视图"
    pass

class LikeView(CommonViewMixin,ListView):
    queryset = Link.objects.filter(status=Link.STATUS_NORMAL)
    template_name = 'config/likes.html'

