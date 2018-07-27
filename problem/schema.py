import graphene
from graphene_django.types import DjangoObjectType
from .models import Problem
from utils.schema import paginatorList


class ProblemType(DjangoObjectType):
    class Meta:
        model = Problem
        only_fields = ('problem_id', 'title', 'content', 'standard_input', 'standard_output',
                       'constraints', 'resource', 'note', 'time_limit', 'memory_limit', 'submit', 'accept', 'slug')
    sample = graphene.JSONString()

    def resolve_sample(self, info, * args, ** kwargs):
        return [{'input': x.input_content, 'output': x.output_content} for x in self.sample_set.all()]


class ProblemListType(graphene.ObjectType):
    class Meta:
        interfaces = (paginatorList, )
    problemList = graphene.List(ProblemType)


class Query(object):
    problem = graphene.Field(ProblemType, slug=graphene.String())
    problemList = graphene.Field(
        ProblemListType, page=graphene.Int(), filter=graphene.String())

    def resolve_problem(self, info, slug):
        _all = Problem.objects.all()
        if not info.context.user.has_perm('problem.view_all'):
            _all = _all.filter(visible=True)
        return _all.get(slug=slug)

    def resolve_problemList(self, info, page, filter=None):
        from django.core.paginator import Paginator
        from Lutece.config import PER_PAGE_COUNT
        problem_list = Problem.objects.all()
        if not info.context.user.has_perm('problem.view_all'):
            problem_list = problem_list.filter(visible=True)
        if filter:
            if filter.startswith('#'):
                nums = filter[1:].split('-')
                if len(nums) == 1 and nums[0].isdigit():
                    problem_list = problem_list.filter(problem_id=nums[0])
                elif len(nums) == 2 and nums[0].isdigit() and nums[1].isdigit():
                    problem_list = problem_list.filter(problem_id__gte=nums[0]).filter(problem_id__lte=nums[1])
                else:
                    problem_list = problem_list.filter(title__icontains=filter)
            else:
                problem_list = problem_list.filter(title__icontains=filter)
        paginator = Paginator(problem_list, PER_PAGE_COUNT)
        return ProblemListType(maxpage=paginator.num_pages, problemList=paginator.get_page(page))


class Mutation(graphene.AbstractType):
    pass
