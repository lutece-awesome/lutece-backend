import graphene
from graphene_django.types import DjangoObjectType
from graphql import ResolveInfo

from data.service import DataService
from problem.limitation.type import AbstractLimiationType
from problem.models import ProblemSample
from utils.interface import PaginatorList


class ProblemSampleType(DjangoObjectType):
    class Meta:
        model = ProblemSample
        only_fields = ("input_content", 'output_content')


class ProblemSampleListType(graphene.ObjectType):
    sample_list = graphene.List(ProblemSampleType, )


class ProblemType(graphene.ObjectType):
    title = graphene.String()
    content = graphene.String()
    resources = graphene.String()
    note = graphene.String()
    slug = graphene.String()
    constraints = graphene.String()
    standard_input = graphene.String()
    standard_output = graphene.String()
    submit = graphene.Int()
    accept = graphene.Int()
    disable = graphene.Boolean()
    pk = graphene.ID()
    limitation = graphene.Field(AbstractLimiationType)
    samples = graphene.Field(ProblemSampleListType)
    data_count = graphene.Int()

    def resolve_title(self, info: ResolveInfo) -> graphene.String():
        return self.title

    def resolve_content(self, info: ResolveInfo) -> graphene.String():
        return self.content

    def resolve_resources(self, info: ResolveInfo) -> graphene.String():
        return self.resources

    def resolve_note(self, info: ResolveInfo) -> graphene.String():
        return self.note

    def resolve_slug(self, info: ResolveInfo) -> graphene.String():
        return self.slug

    def resolve_constraints(self, info: ResolveInfo) -> graphene.String():
        return self.constraints

    def resolve_standard_input(self, info: ResolveInfo) -> graphene.String():
        return self.standard_input

    def resolve_standard_output(self, info: ResolveInfo) -> graphene.String():
        return self.standard_output

    def resolve_standard_submit(self, info: ResolveInfo) -> graphene.Int():
        return self.submit

    def resolve_standard_accept(self, info: ResolveInfo) -> graphene.Int():
        return self.accept

    def resolve_disable(self, info: ResolveInfo) -> graphene.Boolean():
        return self.disable

    def resolve_pk(self, info: ResolveInfo) -> graphene.ID():
        return self.pk

    def resolve_limitation(self, info: ResolveInfo) -> graphene.Field(AbstractLimiationType):
        return self.limitation

    def resolve_samples(self, info: ResolveInfo) -> graphene.Field(ProblemSampleListType):
        result = ProblemSample.objects.filter(problem=self)
        return ProblemSampleListType(sample_list=result)

    def resolve_data_count(self, info: ResolveInfo) -> graphene.Int:
        return DataService.get_cases_count(self.pk)


class ProblemListType(graphene.ObjectType, interfaces=[PaginatorList]):
    problem_list = graphene.List(ProblemType, )
