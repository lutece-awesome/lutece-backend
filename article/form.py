from annoying.functions import get_object_or_None
from django import forms

from article.base.form import AbstractArticleForm
from article.constant import MAX_PREVIEW_LENGTH
from article.models import Article


class UpdateHomeArticleForm(AbstractArticleForm):
    preview = forms.CharField(required=False, max_length=MAX_PREVIEW_LENGTH)
    slug = forms.CharField(required=True)

    def clean(self) -> dict:
        cleaned_data = super().clean()
        slug = cleaned_data.get('slug')
        if not slug or not get_object_or_None(Article, slug=slug):
            self.add_error("slug", "No such home article")
        return cleaned_data


class CreateHomeArticleForm(AbstractArticleForm):
    preview = forms.CharField(required=False, max_length=MAX_PREVIEW_LENGTH)
