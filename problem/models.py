from django.db import models
from problem.baseproblem.models import AbstractProblem
from problem.limitation.models import Limitation
from problem.sample.models import AbstractSample

class Problem( AbstractProblem ):
    submit = models.IntegerField( default = 0 )
    accept = models.IntegerField( default = 0 )
    limitation = models.OneToOneField( Limitation , on_delete = models.CASCADE )

class ProblemSample( AbstractSample ):
    problem = models.ForeignKey( Problem , on_delete = models.SET_NULL , null = True )