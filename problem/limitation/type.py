from graphene_django.types import DjangoObjectType

from problem.limitation.models import Limitation


class AbstractLimiationType(DjangoObjectType):
    class Meta:
        model = Limitation
        only_fields = ("time_limit", "memory_limit", "output_limit", "cpu_limit")
