from django.db import models

from judge.checker import Checker
from problem.base.models import AbstractProblem
from problem.constant import MAX_CHECKER_LENGTH
from problem.limitation.models import Limitation
from problem.sample.models import AbstractSample


class Problem(AbstractProblem):
    submit = models.IntegerField(default=0)
    accept = models.IntegerField(default=0)
    limitation = models.OneToOneField(Limitation, on_delete=models.CASCADE)
    _checker = models.CharField(choices=((each.full, each.info) for each in Checker.all()),
                                max_length=MAX_CHECKER_LENGTH, db_index=True, default=Checker.WCMP.full)

    def ins_submit_times(self):
        self.submit += 1
        self.save()

    def ins_accept_times(self):
        self.accept += 1
        self.save()

    @property
    def checker(self):
        return Checker.value_of(self._checker)


class ProblemSample(AbstractSample):
    problem = models.ForeignKey(Problem, on_delete=models.SET_NULL, null=True)
