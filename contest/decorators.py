from annoying.functions import get_object_or_None
from graphql import GraphQLError

from contest.models import Contest, ContestTeamMember


def check_contest_permission(func):
    def wrapper(*args, **kwargs):
        info = args[func.__code__.co_varnames.index('info')]
        pk = info.variable_values.get('pk')
        contest = get_object_or_None(Contest, pk=pk)
        usr = info.context.user
        if not contest:
            raise GraphQLError('No such contest')
        else:
            privilege = usr.has_perm('contest.view_contest')
            member = None
            if usr.is_authenticated:
                member = get_object_or_None(ContestTeamMember, user=usr, contest_team__contest=contest, confirmed=True)
            if privilege or contest.is_public() or (
                    usr.is_authenticated and member and member.contest_team.approved):
                return func(*args, **kwargs)
            else:
                raise GraphQLError('Permission Denied')

    return wrapper
