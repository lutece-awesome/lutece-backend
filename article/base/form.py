from django import forms

from article.base.constant import MAX_TITLE_LENGTH, MAX_CONTENT_LENGTH


class AbstractArticleForm(forms.Form):
    title = forms.CharField(required=True, max_length=MAX_TITLE_LENGTH)
    content = forms.CharField(required=False, max_length=MAX_CONTENT_LENGTH)
    disable = forms.BooleanField(required=False)
