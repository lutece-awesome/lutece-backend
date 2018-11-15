import graphene
from django.db.models import Q
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import permission_required

from utils.schema import PaginatorList
from .form import UpdateProblemForm
from .models import Problem, Sample


class ProblemType(DjangoObjectType):
    class Meta:
        model = Problem
        only_fields = (
        'problem_id', 'title', 'content', 'standard_input', 'standard_output', 'visible', 'discussionvisible',
        'constraints', 'resource', 'note', 'time_limit', 'memory_limit', 'submit', 'accept', 'slug', 'sample_set')


class SampleType(DjangoObjectType):
    class Meta:
        model = Sample


class ProblemListType(graphene.ObjectType):
    class Meta:
        interfaces = (PaginatorList,)

    problemList = graphene.List(ProblemType)


class UpdateProblem(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        content = graphene.String(required=True)
        standard_input = graphene.String(required=True)
        standard_output = graphene.String(required=True)
        constraints = graphene.String(required=True)
        resource = graphene.String(required=True)
        note = graphene.String(required=True)
        time_limit = graphene.Int(required=True)
        memory_limit = graphene.Int(required=True)
        visible = graphene.Boolean(required=True)
        discussionvisible = graphene.Boolean(required=True)
        slug = graphene.String(required=True)
        samples = graphene.String(required=True)

    state = graphene.Boolean()

    @permission_required('problem.change_problem')
    def mutate(self, info, **kwargs):
        from json import loads
        updateProblemForm = UpdateProblemForm(kwargs)
        if updateProblemForm.is_valid():
            values = updateProblemForm.cleaned_data
            slug, samples = values['slug'], loads(values['samples'])
            values.pop('slug')
            values.pop('samples')
            Problem.objects.filter(slug=slug).update(**values)
            prob = Problem.objects.get(slug=slug)
            prob.sample_set.all().delete()
            for x in samples:
                Sample(
                    input_content=x['input'],
                    output_content=x['output'],
                    problem=prob
                ).save()
            return UpdateProblem(state=True)
        else:
            raise RuntimeError(updateProblemForm.errors.as_json())


class Query(object):
    problem = graphene.Field(ProblemType, slug=graphene.String())
    problemList = graphene.Field(
        ProblemListType, page=graphene.Int(), filter=graphene.String())
    problemSearch = graphene.Field(ProblemListType, filter=graphene.String())

    def resolve_problem(self, info, slug):
        _all = Problem.objects.all()
        if not info.context.user.has_perm('problem.view_all'):
            _all = _all.filter(visible=True)
        return _all.get(slug=slug)

    def resolve_problemList(self, info, page, **kwargs):
        from django.core.paginator import Paginator
        from Lutece.config import PER_PAGE_COUNT
        filter = kwargs.get('filter')
        problem_list = Problem.objects.all()
        if not info.context.user.has_perm('problem.view_all'):
            problem_list = problem_list.filter(visible=True)
        if filter is not None:
            problem_list = problem_list.filter(Q(problem_id__contains=filter) | Q(
                title__icontains=filter) | Q(resource__icontains=filter))
        paginator = Paginator(problem_list, PER_PAGE_COUNT)
        return ProblemListType(maxpage=paginator.num_pages, problemList=paginator.get_page(page))

    def resolve_problemSearch(self, info, **kwargs):
        filter = kwargs.get('filter')
        problem_list = Problem.objects.all()
        if not info.context.user.has_perm('problem.view_all'):
            problem_list = problem_list.filter(visible=True)
        if not filter:
            problem_list = problem_list.filter(title__icontains=filter)
        return ProblemListType(maxpage=1, problemList=problem_list[:5])


class Mutation(graphene.AbstractType):
    UpdateProblem = UpdateProblem.Field()
