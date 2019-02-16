import graphene
from graphql import ResolveInfo
from graphql_jwt.decorators import permission_required
from json import loads

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

    state = graphene.Boolean()

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
            return UpdateProblem(state=True)
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
            print(samples)
            for each in samples:
                ProblemSample(
                    input_content=each.get('inputContent'),
                    output_content=each.get('outputContent'),
                    problem=prob
                ).save()
            return CreateProblem(slug=prob.slug)
        else:
            raise RuntimeError(form.errors.as_json())


class Mutation(graphene.AbstractType):
    update_problem = UpdateProblem.Field()
    create_problem = CreateProblem.Field()
