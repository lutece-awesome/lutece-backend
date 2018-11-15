from django.contrib.auth.models import AbstractUser
from django.db import models

from problem.models import Problem
from user.attachinfo.models import AttachInfo


class User(AbstractUser):
    attach_info = models.OneToOneField(AttachInfo, on_delete=models.CASCADE)
    solved = models.IntegerField(default=0)
    tried = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f'<User:{self.username}>'

    def refresh_solve(self):
        self.tried = Solve.objects.filter(user=self).count()
        self.solved = Solve.objects.filter(user=self, status=True).count()
        self.save()


class Solve(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    problem = models.ForeignKey(Problem, on_delete=models.SET_NULL, null=True)
    status = models.BooleanField(default=False)
