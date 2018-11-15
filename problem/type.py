import graphene
from graphene_django.types import DjangoObjectType

from data.service import DataService
from problem.limitation.type import AbstractLimiationType
from problem.models import Problem, ProblemSample
from utils.interface import PaginatorList


class ProblemSampleType(DjangoObjectType):
    class Meta:
        model = ProblemSample
        only_fields = ("input_content", 'output_content')


class ProblemSampleListType(graphene.ObjectType):
    sample_list = graphene.List(ProblemSampleType, )


class ProblemType(DjangoObjectType):
    class Meta:
        model = Problem
        only_fields = (
        'title', 'content', 'resources', 'constraints', 'note', 'slug', 'standard_input', 'standard_output', 'submit',
        'accept', 'disable')

    pk = graphene.ID()
    limitation = graphene.Field(AbstractLimiationType)
    samples = graphene.Field(ProblemSampleListType)
    data_count = graphene.Int()

    def resolve_pk(self, info, *args, **kwargs):
        return self.pk

    def resolve_limitation(self, info, *args, **kwargs):
        return self.limitation

    def resolve_samples(self, info, *args, **kwargs):
        result = ProblemSample.objects.filter(problem=self)
        return ProblemSampleListType(sample_list=result)

    def resolve_data_count(self, info, *args, **kwargs):
        return DataService.get_cases_count(self.pk)


class ProblemListType(graphene.ObjectType):
    class Meta:
        interfaces = (PaginatorList,)

    problem_list = graphene.List(ProblemType, )
