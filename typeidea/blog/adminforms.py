# 文章内容中的 '摘要' 部分的输入框样式，变成自定义的样式

from django import forms

class PostAdminForm(forms.ModelForm):
    desc = forms.CharField(widget=forms.Textarea, label='摘要', required=False)