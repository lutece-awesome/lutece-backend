import graphene
from user.attachinfo.type import AttachInfoType
from utils.interface import paginatorList

class UserType( graphene.ObjectType ):
    username = graphene.String()
    joined_date = graphene.Date()
    lastlogin_date = graphene.DateTime()
    attach_info = graphene.Field( AttachInfoType )

    def resolve_username( self , info , * args , ** kwargs ):
        return self.username

    def resolve_joined_date( self , info , * args , ** kwargs ):
        return self.date_joined.date()
    
    def resolve_lastlogin_date( self , info , * args , ** kwargs ):
        return self.last_login or self.date_joined
    
    def resolve_attach_info( self , info , * args , ** kwargs ):
        return self.attach_info

class UserListType( graphene.ObjectType ):
    class Meta:
        interfaces = ( paginatorList, )
    userList = graphene.List( UserType )

