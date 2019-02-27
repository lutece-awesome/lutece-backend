from annoying.functions import get_object_or_None
from graphql import GraphQLError

from contest.models import Contest, ContestTeamMember


def check_contest_permission(func):
    def wrapper(*args, **kwargs):
        info = args[func.__code__.co_varnames.index('info')]
        pk = args[func.__code__.co_varnames.index('pk')]
        contest = get_object_or_None(Contest, pk=pk)
        usr = info.context.user
        if not contest:
            raise GraphQLError('No such contest')
        elif not usr.has_perm('contest.view') and not get_object_or_None(ContestTeamMember, user=usr,
                                                                         contest_team__contest=contest):
            raise GraphQLError('Permission Denied')
        check_contest_permission(*args, **kwargs)

    return wrapper
