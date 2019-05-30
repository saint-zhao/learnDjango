from django import forms
import mistune
#from django.forms import widgets

from .models import Comment

class CommentForm(forms.ModelForm):
    nickname = forms.CharField(
        label='昵称',
        max_length=50,
        widget=forms.widgets.Input(
            attrs={'class':'form-control', 'style':'width:60%;'}
        )
    )

    content = forms.CharField(
        label='评论内容',
        max_length=500,
        widget=forms.widgets.Textarea(
            attrs={'rows':6, 'cols':60, 'class':'form-control'}
        )
    )

    email = forms.CharField(
        label='邮箱',
        max_length=50,
        widget=forms.widgets.EmailInput(
            attrs={'class':'form-control', 'style':'width:60%;'}
        )
    )

    website = forms.CharField(
        label='网站',
        max_length=128,
        widget=forms.widgets.URLInput(
            attrs={'class':'form-control', 'style':'width:60%'}
        )
    )

    def clean_content(self):
        content = self.cleaned_data.get('content')
        content = mistune.markdown(content) # 增加markdown支持

        if len(content) < 10:
            raise forms.ValidationError('内容不能少于10个字。')
        return content

    class Meta:
        model = Comment
        fields = (
            'nickname', 'email', 'website', 'content'
        )
