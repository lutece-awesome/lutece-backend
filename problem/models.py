from django.db import models
from problem.baseproblem.models import AbstractProblem
from problem.limitation.models import Limitation

class ClassicProblem( AbstractProblem ):
    limiation = models.OneToOneField( Limitation , on_delete = models.CASCADE )
    