import graphene
from user.attachinfo.type import AttachInfoType
from utils.interface import PaginatorList

class UserType( graphene.ObjectType ):
    pk = graphene.ID()
    username = graphene.String()
    joined_date = graphene.Date()
    last_login_date = graphene.DateTime()
    attach_info = graphene.Field( AttachInfoType )

    def resolve_pk( self , info , * args , ** kwargs ):
        return self.pk

    def resolve_username( self , info , * args , ** kwargs ):
        return self.username

    def resolve_joined_date( self , info , * args , ** kwargs ):
        return self.date_joined.date()
    
    def resolve_last_login_date( self , info , * args , ** kwargs ):
        return self.last_login or self.date_joined
    
    def resolve_attach_info( self , info , * args , ** kwargs ):
        return self.attach_info

class UserListType( graphene.ObjectType ):
    class Meta:
        interfaces = ( PaginatorList, )
    user_list = graphene.List( UserType )