import graphene
from problem.baseproblem.type import AbstractProblemType
from problem.limitation.type import LimiationType

class ProblemType( AbstractProblemType ):
    
    limitation = graphene.Field( LimiationType )

    def resolve_limitation( self , info , * args , ** kwargs ):
        return self.limitation