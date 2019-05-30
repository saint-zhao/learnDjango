from django.shortcuts import render, redirect
from django.views.generic import ListView, TemplateView

from .forms import CommentForm

# Create your views here.

class CommentView(TemplateView):
    http_method_names = ['post']
    template_name = 'comment/result.html'

    def post(self, request, *args, **kwargs):
        comment = CommentForm(request.POST)
        target = request.POST.get('target')
        print('数据待验证')
        if comment.is_valid():
            print('数据验证通过')
            instance = comment.save(commit=False)
            instance.target = target
            instance.save()

            succeed = True
            print(111, succeed)
            return redirect(target)
        else:
            succeed = False
        print(comment.errors.items(),11111)
        context = {
            'succeed': succeed,
            'form': comment,
            'target': target,
        }
        return self.render_to_response(context)


