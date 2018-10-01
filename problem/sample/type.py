import graphene
from graphene_django.types import DjangoObjectType
from problem.sample.models import AbstractSample
from utils.interface import PaginatorList

class AbstractSampleType( DjangoObjectType ):
    class Meta:
        model = AbstractSample
        only_fields = ( "input_content" , 'output_content' )


class AbstractSampleListType( graphene.ObjectType ):
    class Meta:
        interfaces = ( PaginatorList , )
    sample_list = graphene.List( AbstractSample , )