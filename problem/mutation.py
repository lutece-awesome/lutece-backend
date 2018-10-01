import graphene
from json import loads
from problem.form import UpdateProblemForm, CreateProblemForm
from problem.models import Problem, ProblemSample
from utils.function import assign
from graphql_jwt.decorators import permission_required

class UpdateProblem(graphene.Mutation):

    class Arguments:
        title = graphene.String( required = True )
        content = graphene.String( required = True )
        resources = graphene.String( required = True )
        constraints = graphene.String( required = True )
        note = graphene.String( required = True )
        
        time_limit = graphene.Int( required = True )
        memory_limit = graphene.Int( required = True )
        output_limit = graphene.Int( required = True )
        cpu_limit = graphene.Int( required = True )

        samples = graphene.String( required = True )
        
    state = graphene.Boolean()

    @permission_required( 'AbstractProblem.change' )
    def mutate( self , info , ** kwargs ):
        form = UpdateProblemForm( kwargs )
        if form.is_valid():
            values = form.cleaned_data
            samples = loads( values.get( 'samples') )
            prob = Problems.objects.get( title = values.get( 'title' ) )
            assign( prob , ** values )
            assign( prob.limiation , ** values )
            prob.limiation.save()
            prob.save()
            ProblemSample.objects.filter( problem = prob ).delete()
            for each in samples:
                ProblemSample(
                    input_content = each.get( 'input_content' ),
                    output_content = each.get( 'output_content' ),
                    problem = prob
                ).save()
            return UpdateProblem( state = True )
        else:
            raise RuntimeError( form.errors.as_json() )

class CreateProblem( UpdateProblem ):

    @permission_required( 'AbstractProblem.add' )
    def mutate( self , info , ** kwargs ):
        form = CreateProblemForm( kwargs )
        if form.is_valid():
            values = form.cleaned_data
            samples = loads( values.get( 'samples') )
            prob = Problem()
            assign( prob , ** values )
            assign( prob.limiation , ** values )
            prob.limiation.save()
            prob.save()
            ProblemSample.objects.filter( problem = prob ).delete()
            for each in samples:
                ProblemSample(
                    input_content = each.get( 'input_content' ),
                    output_content = each.get( 'output_content' ),
                    problem = prob
                ).save()
            return CreateProblem( state = True )
        else:
            raise RuntimeError( form.errors.as_json() )

class Mutation(graphene.AbstractType):
    update_problem = UpdateProblem.Field()
    create_problem = CreateProblem.Field()