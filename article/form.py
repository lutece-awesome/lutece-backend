from django import forms

from article.base.form import AbstractArticleForm
from article.constant import MAX_PREVIEW_LENGTH


class HomeArticleForm(AbstractArticleForm):
    preview = forms.CharField(required=False, max_length=MAX_PREVIEW_LENGTH)

    def clean(self) -> dict:
        return super().clean()
