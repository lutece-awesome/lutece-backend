import graphene
from user.type import UserType, UserListType
from user.models import User
from django.core.paginator import Paginator
from user.constant import PER_PAGE_COUNT


class Query( object ):

    user = graphene.Field( UserType , username = graphene.String() )
    user_list = graphene.Field( UserListType , filter = graphene.String() , page = graphene.Int() )

    def resolve_user( self , info , * args , ** kwargs ):
        return User.objects.get( username = kwargs.get( 'username' ) )

    def resolve_user_list( self , info , * args , ** kwargs ):
        page = kwargs.get( 'page' )
        filter = kwargs.get('filter')
        user_list = User.objects.all().filter( is_active = True , is_staff = False )
        if filter:
            user_list = user_list.filter( username__icontains = filter )
        paginator = Paginator (user_list , PER_PAGE_COUNT )
        return UserListType( maxpage = paginator.num_pages, user_list = paginator.get_page( page ) )