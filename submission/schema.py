import graphene
from graphene_django.types import DjangoObjectType
from annoying.functions import get_object_or_None
from problem.models import Problem
from .models import Submission
from graphql_jwt.decorators import login_required

class SubmitSolution( graphene.Mutation ):

    class Arguments:
        problemslug = graphene.String( required = True )
        code = graphene.String( required = True )
        language = graphene.String( required = True )
    
    state = graphene.Boolean()
    
    @login_required
    def mutate( self , info , ** kwargs ):
        from .form import SubmitSolutionForm
        from data_server.util import get_case_number
        from submission.judge_result import Judge_result
        from problem.util import InsSubmittimes
        from Lutece.settings import TASK_QUEUE
        SolutionForm = SubmitSolutionForm( kwargs )
        if SolutionForm.is_valid():
            values = SolutionForm.cleaned_data
            problem = get_object_or_None( Problem , slug = values['problemslug'] )
            s = Submission(
                language = values['language'],
                user = info.context.user,
                problem = problem,
                case_number = get_case_number( problem.pk ),
                judge_status = Judge_result.PD.value.full,
                code = values['code'])
            s.save()
            Submission_task.apply_async( args = (s.get_push_dict() ,) , queue = TASK_QUEUE )
            InsSubmittimes( problem.pk )
            return SubmitSolution( state = True )
        else:
            raise RuntimeError( SolutionForm.errors.as_json() )


class Query( object ):
    pass

class Mutation( graphene.AbstractType ):
    SubmitSolution = SubmitSolution.Field()