from django.db import models

from article.base.models import AbstractArticle
from record.models import SimpleRecord


# The base class of all sub-class of article
class Article(AbstractArticle):

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


# The home page article model
class HomeArticle(Article):
    preview = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


# The user article model
class UserArticle(Article):
    pass


class ArticleRecord(SimpleRecord):
    article = models.ForeignKey(Article, null=True, on_delete=models.SET_NULL)
