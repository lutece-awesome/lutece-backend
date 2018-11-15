from django.db import models

from problem.limitation.constant import DEFAULT_TIME_LIMIT, DEFAULT_MEMORY_LIMIT, DEFAULT_OUTPUT_LIMIT, \
    DEFAULT_CPU_NUMBER


class Limitation(models.Model):
    time_limit = models.PositiveIntegerField(default=DEFAULT_TIME_LIMIT)
    memory_limit = models.PositiveIntegerField(default=DEFAULT_MEMORY_LIMIT)
    output_limit = models.PositiveIntegerField(default=DEFAULT_OUTPUT_LIMIT)
    cpu_limit = models.PositiveIntegerField(default=DEFAULT_CPU_NUMBER)
