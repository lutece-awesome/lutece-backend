from django.db import models

from judge.constant import MAX_RESULT_LENGTH, MAX_COMPILE_LENGTH, MAX_ERROR_LENGTH
from judge.result import JudgeResult as JudgeResultService


class JudgeResult(models.Model):
    _result = models.CharField(choices=((each.full, each.detail) for each in JudgeResultService.all()),
                               max_length=MAX_RESULT_LENGTH, db_index=True)
    compile_info = models.CharField(max_length=MAX_COMPILE_LENGTH, blank=True)
    error_info = models.CharField(max_length=MAX_ERROR_LENGTH, blank=True)
    done = models.BooleanField(default=False)

    @property
    def result(self, *args, **kwargs):
        return JudgeResultService.value_of(self._result)
