import graphene
from judge.result import JudgeResult

class JudgeResultType( graphene.ObjectType ):
    full = graphene.String()
    alias = graphene.String()
    color = graphene.String()
    detail = graphene.String()

    def resolve_full( self , info , * args , ** kwargs ):
        return self.full

    def resolve_alias( self , info , * args , ** kwargs ):
        return self.alias

    def resolve_color( self , info , * args , ** kwargs ):
        return self.color

    def resolve_detail( self , info , * args , ** kwargs ):
        return self.detail