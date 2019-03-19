import graphene
from graphene_file_upload.scalars import Upload
from graphql import ResolveInfo
from graphql_jwt.decorators import permission_required
from json import loads

from data.service import DataService
from problem.form import UpdateProblemForm, CreateProblemForm
from problem.limitation.models import Limitation
from problem.models import Problem, ProblemSample
from utils.function import assign


class UpdateProblem(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        standard_input = graphene.String(required=True)
        standard_output = graphene.String(required=True)
        content = graphene.String(required=True)
        resources = graphene.String(required=True)
        constraints = graphene.String(required=True)
        note = graphene.String(required=True)

        time_limit = graphene.Int(required=True)
        memory_limit = graphene.Int(required=True)
        output_limit = graphene.Int(required=True)
        cpu_limit = graphene.Int(required=True)

        samples = graphene.String(required=True)

        disable = graphene.Boolean(required=True)

        slug = graphene.String(required=True)

    slug = graphene.String()

    @permission_required('problem.change')
    def mutate(self, info: ResolveInfo, **kwargs):
        form = UpdateProblemForm(kwargs)
        if form.is_valid():
            values = form.cleaned_data
            samples = loads(values.get('samples'))
            prob = Problem.objects.get(slug=values.get('slug'))
            assign(prob, **values)
            assign(prob.limitation, **values)
            prob.limitation.save()
            prob.save()
            ProblemSample.objects.filter(problem=prob).delete()
            for each in samples:
                ProblemSample(
                    input_content=each.get('inputContent'),
                    output_content=each.get('outputContent'),
                    problem=prob
                ).save()
            # To avoid the slug change, re-fetch the problem object
            return UpdateProblem(slug=prob.slug)
        else:
            raise RuntimeError(form.errors.as_json())


class CreateProblem(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        content = graphene.String(required=False)
        resources = graphene.String(required=False)
        constraints = graphene.String(required=False)
        note = graphene.String(required=False)
        standard_input = graphene.String(required=False)
        standard_output = graphene.String(required=False)

        time_limit = graphene.Int(required=True)
        memory_limit = graphene.Int(required=True)
        output_limit = graphene.Int(required=True)
        cpu_limit = graphene.Int(required=True)

        disable = graphene.Boolean(required=True)

        samples = graphene.String(required=True)

    slug = graphene.String()

    @permission_required('problem.add')
    def mutate(self, info: ResolveInfo, **kwargs):
        form = CreateProblemForm(kwargs)
        if form.is_valid():
            values = form.cleaned_data
            samples = loads(values.get('samples'))
            prob = Problem()
            limitation = Limitation()
            assign(prob, **values)
            assign(limitation, **values)
            limitation.save()
            prob.limitation = limitation
            prob.save()
            for each in samples:
                ProblemSample(
                    input_content=each.get('inputContent'),
                    output_content=each.get('outputContent'),
                    problem=prob
                ).save()
            return CreateProblem(slug=prob.slug)
        else:
            raise RuntimeError(form.errors.as_json())


class UpdateProblemData(graphene.Mutation):
    class Arguments:
        pk = graphene.ID(required=True)
        file = Upload(required=True)

    state = graphene.Boolean()

    @permission_required('problem.change')
    def mutate(self, info: ResolveInfo, **kwargs):
        try:
            file = kwargs.get('file')
            pk = kwargs.get('pk')
            DataService.check_datazip(file)
            DataService.clear_folder_and_extract_data(pk, file)
        except Exception as e:
            raise RuntimeError(str(e))


class Mutation(graphene.AbstractType):
    update_problem = UpdateProblem.Field()
    create_problem = CreateProblem.Field()
    update_problem_data = UpdateProblemData.Field()
