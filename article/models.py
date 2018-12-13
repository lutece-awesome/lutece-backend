from django.db import models

from article.base.models import AbstractArticle
from record.models import SimpleRecord


class Article(AbstractArticle):

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


'''
    Home article permission: article.<add/change/delete>_homearticle
'''


class HomeArticle(Article):
    preview = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class ArticleRecord(SimpleRecord):
    article = models.ForeignKey(Article, null=True, on_delete=models.SET_NULL)
