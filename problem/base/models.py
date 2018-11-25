from django.db import models
from uuslug import uuslug

from problem.base.constant import MAX_TITLE_LENGTH, MAX_CONTENT_LENGTH, MAX_RESOURCES_LENGTH, \
    MAX_CONSTRAINTS_LENGTH, MAX_NOTE_LENGTH, MAX_STANDARD_INPUT_LENGTH, MAX_STANDARD_OUTPUT_LENGTH, MAX_SLUG_LENGTH


class AbstractProblem(models.Model):
    class Meta:
        abstract = True

    title = models.CharField(max_length=MAX_TITLE_LENGTH, db_index=True)
    content = models.TextField(max_length=MAX_CONTENT_LENGTH, blank=True)
    resources = models.CharField(max_length=MAX_RESOURCES_LENGTH, blank=True)
    constraints = models.TextField(max_length=MAX_CONSTRAINTS_LENGTH, blank=True)
    standard_input = models.TextField(max_length=MAX_STANDARD_INPUT_LENGTH, blank=True)
    standard_output = models.TextField(max_length=MAX_STANDARD_OUTPUT_LENGTH, blank=True)
    note = models.TextField(max_length=MAX_NOTE_LENGTH, blank=True)
    slug = models.CharField(max_length=MAX_SLUG_LENGTH)
    disable = models.BooleanField(default=False)

    def __str__(self):
        return f'<Problem:{self.title}>'

    def __unicode__(self):
        return f'<Problem:{self.title}>'

    def save(self, *args, **kwargs):
        self.slug = uuslug(self.title, instance=self)
        super().save(*args, **kwargs)
