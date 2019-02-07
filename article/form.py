from annoying.functions import get_object_or_None
from django import forms

from article.base.form import AbstractArticleForm
from article.constant import MAX_PREVIEW_LENGTH
from article.models import HomeArticle, UserArticle, Article


class UpdateHomeArticleForm(AbstractArticleForm):
    preview = forms.CharField(required=False, max_length=MAX_PREVIEW_LENGTH)
    slug = forms.CharField(required=True)

    def clean(self) -> dict:
        cleaned_data = super().clean()
        slug = cleaned_data.get('slug')
        if not slug or not get_object_or_None(HomeArticle, slug=slug):
            self.add_error("slug", "No such home article")
        return cleaned_data


class CreateHomeArticleForm(AbstractArticleForm):
    preview = forms.CharField(required=False, max_length=MAX_PREVIEW_LENGTH)


class CreateUserArticleForm(AbstractArticleForm):
    pass


class UpdateUserArticleForm(AbstractArticleForm):
    pk = forms.IntegerField(required=True)

    def clean(self) -> dict:
        cleaned_data = super().clean()
        pk = cleaned_data.get('pk')
        if pk and not get_object_or_None(UserArticle, pk=pk):
            self.add_error("pk", "No such user article")
        return cleaned_data


class UpdateArticleRecordForm(forms.Form):
    pk = forms.IntegerField(required=True)

    def clean(self) -> dict:
        cleaned_data = super().clean()
        pk = cleaned_data.get('pk')
        if pk and not get_object_or_None(Article, pk=pk):
            self.add_error("pk", "No such article")
        return cleaned_data
