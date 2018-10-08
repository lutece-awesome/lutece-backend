import graphene
from graphene.types.generic import GenericScalar
from judge.result import JudgeResult
from submission.models import Submission
from user.models import Solve
from graphene_django.types import DjangoObjectType


class UserSolveType( DjangoObjectType ):
    class Meta:
        model = Solve
        only_fields = ( 'status' )
    
    pk = graphene.ID()
    slug = graphene.String()

    def resolve_pk( self , info , * args , ** kwargs ):
        return self.problem.pk
    
    def resolve_slug( self , info , * args , ** kwargs ):
        return self.problem.slug

class UserSubmissionStatisticsType( graphene.ObjectType ):
    ac = graphene.Int()
    tle = graphene.Int()
    ce = graphene.Int()
    wa = graphene.Int()
    re = graphene.Int()
    ole = graphene.Int()
    mle = graphene.Int()
    ratio = graphene.Float()
    solve = graphene.List( UserSolveType )

    def __init__( self , * args , ** kwargs ):
        if 'user' in kwargs:
            self.user = kwargs['user']
        else:
            raise RuntimeError( 'User field is required' )

    def resolve_ac( self , info , * args , ** kwargs ):
        return Submission.objects.filter( user = self.user , result___result = JudgeResult.AC.full  ).count()

    def resolve_tle( self , info , * args , ** kwargs ):
        return Submission.objects.filter( user = self.user , result___result = JudgeResult.TLE.full  ).count()
    
    def resolve_ce( self , info , * args , ** kwargs ):
        return Submission.objects.filter( user = self.user , result___result = JudgeResult.CE.full  ).count()
    
    def resolve_wa( self , info , * args , ** kwargs ):
        return Submission.objects.filter( user = self.user , result___result = JudgeResult.WA.full  ).count()

    def resolve_re( self , info , * args , ** kwargs ):
        return Submission.objects.filter( user = self.user , result___result = JudgeResult.RE.full  ).count()

    def resolve_ole( self , info , * args , ** kwargs ):
        return Submission.objects.filter( user = self.user , result___result = JudgeResult.OLE.full  ).count()

    def resolve_mle( self , info , * args , ** kwargs ):
        return Submission.objects.filter( user = self.user , result___result = JudgeResult.MLE.full  ).count()
    
    def resolve_ratio( self , info , * args , ** kwargs ):
        ac = self.resolve_ac( info , * args , ** kwargs )
        all = Submission.objects.filter( user = self.user ).count()
        return ac / all if all else 0

    def resolve_solve( self , info , * args , ** kwargs ):
        obj = Solve.objects.filter( user = self.user ).order_by( 'problem__pk' )
        return list( obj )