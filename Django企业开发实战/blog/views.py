from django.shortcuts import render, HttpResponse ,get_object_or_404
from django.views.generic import DetailView, ListView  # 类视图

from .models import Post, Tag, Category
from config.models import SideBar

# Create your views here.

def post_list(request,category_id=None,tag_id=None):
    "这个汉书是根据分类或者标签或者显示首页所有文章的试图函数"
    tag = None
    category = None
    if tag_id:
        post_list, tag = Post.get_by_tag(tag_id)
        # 下面这一块整合到模型里面去了
        # try:
        #     tag = Tag.objects.get(id=tag_id)
        # except tag.DoesNotExist:
        #     post_list = []
        # else:
        #     post_list = Tag.tag_post.filter(status=Post.STATUS_NORMAL)

    elif category_id:
        post_list, category = Post.get_by_category(category_id)

    else:
        post_list = Post.latest_posts()
        # 下面这一块已经整合到models里面
        # post_list = Post.objects.filter(status=Post.STATUS_NORMAL)
        # if category_id:
        #     post_list = post_list.filter(category_id=category_id)
    context = {
        'category':category,
        'tag':tag,
        'post_list':post_list,
        'sidebars':SideBar.get_all(),
    }
    context.update(Category.get_nav())

    return render(request, 'blog/post_list.html', context=context)

# 下面使用类视图重写post_list函数
class CommonViewMixin:
    """在这个类里面定义了给内容里面添加导航数据以及侧边栏数据"""
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'sidebars': SideBar.get_all()})
        context.update(Category.get_nav())
        return context


class PostListView(CommonViewMixin,ListView):
    """这是显示说有文章的类"""
    queryset = Post.latest_posts()
    paginate_by = 1  # 设置一页展示多少文章
    context_object_name = 'post_list'  # 设置模板变量
    template_name = 'blog/post_list.html'


class CategoryView(PostListView):
    """这是显示分类所有posts的视图"""
    def get_context_data(self,**kwargs):
        """这个是获取渲染到模板的上下文"""
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, pk=category_id)
        context.update({
            'category':category,
        })
        return context

    def get_queryset(self):
        """重写querset，根据分类过滤"""
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category__id=category_id)


class TagView(PostListView):
    """这是显示标签的所有posts"""
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get('tag_id')
        tag = get_object_or_404(Tag, pk=tag_id)
        context.update({
            'tag':tag
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        tag_id = self.kwargs.get('tag_id')
        return queryset.filter(tag_id=tag_id)


def post_detail(request,post_id=None):
    """显示文章具体内容的视图"""
    try:
        post = Post.objects.get(id=post_id)
    except post.DoesNotExist:
        post = None

    return render(request,'blog/post_detal.html',context={'post':post})

# 下面这个是使用类视图重写post_detail函数,它内部自己实现了get方法
class PostDetailView(CommonViewMixin,DetailView):
    queryset = Post.latest_posts()
    template_name = 'blog/post_detal.html'
    context_object_name = 'post'  #设置模板里面的变量显示
    pk_url_kwarg = 'post_id'