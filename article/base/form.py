from annoying.functions import get_object_or_None
from django import forms

from article.base.constant import MAX_TITLE_LENGTH, MAX_CONTENT_LENGTH
from user.models import User


class AbstractArticleForm(forms.Form):
    title = forms.CharField(required=True, max_length=MAX_TITLE_LENGTH)
    content = forms.CharField(required=False, max_length=MAX_CONTENT_LENGTH)
    author = forms.CharField(required=True)

    def clean(self) -> dict:
        cleaned_data = super().clean()
        author = cleaned_data.get('user')
        if not get_object_or_None(User, username=author):
            self.add_error('author', f'Unknown user<{ author }>')
        return cleaned_data
