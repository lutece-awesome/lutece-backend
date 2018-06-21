from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Contest
from Lutece import config
from utils.paginator_menu import get_range as page_range
from .contest_type import get_contest_type_list, get_contest_type
from django.http import HttpResponse, Http404
from json import dumps, loads
from annoying.functions import get_object_or_None
from .contest_status import get_contest_status
from datetime import datetime
from .util import check_contest_started_or_has_perms, check_contest_has_perms

# Create your views here.


def get_contest_list( request , page ):
    contest_list = Contest.objects.all()
    if not request.user.has_perm( 'contest.view_all' ):
        contest_list = contest_list.filter( visible = True )
    from .contest_status import get_contest_status
    paginator = Paginator(contest_list, config.PER_PAGE_COUNT)
    contests = paginator.get_page(page)
    page = min( max( 1 , page ) , paginator.num_pages )
    return render(request, 'contest/contest_list.html', {
        'contestlist': contests,
        'conteststatus' : [ get_contest_status( x.start_time , x.end_time ) for x in contests ],
        'currentpage' : page,
        'max_page': paginator.num_pages,
        'contesttypelist' : get_contest_type_list(),
        'page_list' : page_range( page , paginator.num_pages ) })


@permission_required( 'contest.add_contest' )
def create_contest( request ):
    status = {
        'status' : False,
        'error_list': []}
    err = status['error_list']
    try:
        title = request.POST.get( 'title' ).strip()
        from datetime import datetime, timedelta
        start_time = datetime.strptime( request.POST.get( 'start_time' ) , "%Y-%m-%d-%H-%M" )
        end_time = datetime.strptime( request.POST.get( 'end_time' ) , "%Y-%m-%d-%H-%M" )
        contest_type = request.POST.get( 'type' ).strip()
        password = request.POST.get( 'password' )
        if len( title ) == 0:
            err.append( 'Title can not be empty' )
        if get_object_or_None( Contest , title = title ) is not None:
            err.append( 'Title should be unique' )
        if end_time <= start_time:
            err.append( 'Endtime should earlier than starttime')
        if end_time - timedelta( days = 30 ) >= start_time:
            err.append( 'The length of contest should no more than 30 days.' )
        if get_contest_type( contest_type ) is None:
            err.append( 'Unknown contesttype' )
        if len( err ) > 0:
            return
        s = Contest( 
            title = title,
            start_time = start_time,
            end_time = end_time,
            password = password,
            contest_type = contest_type)
        s.save()
        status['contest_id'] = s.pk
        status['status'] = True
    except Exception as e:
        err.append( str( e ) )
    finally:
        return HttpResponse(dumps(status), content_type='application/json')

@permission_required( 'contest.change_contest' )
def edit_contest( request , pk ):
    from problem.models import Problem
    contest = get_object_or_None( Contest , pk = pk )
    return render( request , 'contest/contest_edit.html' , {
        'prob' : [ get_object_or_None( Problem , pk = x.problem ) for x in contest.contestproblem_set.all() ],
        'contest' : contest,
        'contesttypelist' : get_contest_type_list() })


@permission_required( 'contest.change_contest' )
def update_contest( request , pk ):
    status = {
        'status' : False,
        'error_list': []}
    err = status['error_list']
    try:
        title = request.POST.get( 'title' ).strip()
        from datetime import datetime, timedelta
        from problem.models import Problem
        from contest.models import ContestProblem
        start_time = datetime.strptime( request.POST.get( 'start_time' ) , "%Y-%m-%d-%H-%M" )
        end_time = datetime.strptime( request.POST.get( 'end_time' ) , "%Y-%m-%d-%H-%M" )
        contest_type = request.POST.get( 'type' ).strip()
        password = request.POST.get( 'password' )
        note = request.POST.get( 'note' )
        visible = request.POST.get( 'visible' )
        register = request.POST.get( 'register' )
        prob = loads( request.POST.get( 'prob') )
        if len( prob ) > 26:
            err.append( 'The number of contest problem should no more than 26' )
        for each in prob:
            if len( each ) == 0:
                err.append( 'Problem id can not be empty' )
            elif get_object_or_None( Problem , pk = int(each) ) is None:
                err.append( 'Unknown problem id: ' + each )
        if len( prob ) != len( set( prob ) ):
            err.append( 'Problems should unique' )
        if len( title ) == 0:
            err.append( 'Title can not be empty' )
        if end_time <= start_time:
            err.append( 'Endtime should earlier than starttime')
        if end_time - timedelta( days = 30 ) >= start_time:
            err.append( 'The length of contest should no more than 30 days.' )
        if get_contest_type( contest_type ) is None:
            err.append( 'Unknown contesttype' )
        if len( err ) > 0:
            return
        contest = Contest.objects.get( pk = pk )
        contest.contestproblem_set.all().delete()
        for each in prob:
            ContestProblem(
                contest = contest,
                problem = int( each )
            ).save()
        Contest.objects.filter( pk = pk ).update(
            title = title,
            start_time = start_time,
            end_time = end_time,
            password = password,
            contest_type = contest_type,
            visible = True if visible == 'true' else False,
            register = True if register == 'true' else False,
            note = note)
        status['status'] = True
    except Exception as e:
        err.append( str( e ) )
    finally:
        return HttpResponse(dumps(status), content_type='application/json')


def overview_contest( request , pk ):
    contest = get_object_or_None( Contest , pk = pk )
    return render( request , 'contest/contest_overview.html' ,{
        'contest' : contest,
        'contesttype' : get_contest_type( contest.contest_type ),
    })


def get_contest_problem( request , pk , index ):
    from problem.models import Problem
    from utils.language import get_language_list
    contest = get_object_or_None( Contest, pk = pk )
    if not check_contest_started_or_has_perms( contest , request.user ):
        return HttpResponse( 'Contest has not yet started' )
    prob = get_object_or_None( Problem , pk = contest.contestproblem_set.all()[index].problem )
    return render( request , 'contest/contest_problem.html' ,{
        'prob' : prob,
        'support_lang': get_language_list(),
        'sample': prob.sample_set.all(),
        'contest' : contest,})

def get_problem_list( request , pk ):
    from problem.models import Problem
    from .util import get_contest_analysis, get_user_contest_problem_analysis
    contest = get_object_or_None( Contest , pk = pk )
    if not check_contest_started_or_has_perms( contest , request.user ):
        return render( request , 'contest/contest_not_started.html' )
    contest_problem_set = contest.contestproblem_set.all()
    return render( request , 'contest/contest_problem_list.html' , {
        'prob' : [ get_object_or_None( Problem , pk = x.problem ) for x in contest_problem_set ],
        'contest_analysis' : get_contest_analysis( contest ),
        'user_problem_analysis' : [ get_user_contest_problem_analysis( user = request.user , problem = get_object_or_None( Problem , pk = x.problem ) )  for x in contest_problem_set ] if request.user.is_authenticated else None,
        'contest' : contest,})

def get_contest_submission( request , pk , page ):
    from submission.models import Submission
    contest = get_object_or_None( Contest , pk = pk )
    if not check_contest_started_or_has_perms( contest , request.user ):
        return render( request , 'contest/contest_not_started.html' )
    pos_hashtable = { x.problem : i for i , x in enumerate(contest.contestproblem_set.all()) }
    if request.user.is_authenticated:
        if request.user.has_perm( 'contest.view_all' ):
            sub_all = Submission.objects.filter( contest = contest )
        else:
            sub_all = Submission.objects.filter( contest = contest , user = request.user )
    else:
        sub_all = list()
    paginator = Paginator(sub_all, config.PER_PAGE_COUNT)
    statuslist = paginator.get_page(page)
    page = min( max( 1 , page ) , paginator.num_pages )
    return render(request, 'contest/contest_submission.html', {
        'contest' : contest,
        'pos_hashtable' : pos_hashtable,
        'statuslist' : statuslist,
        'currentpage' : page,
        'max_page': paginator.num_pages,
        'page_list' : page_range( page , paginator.num_pages ) })

def get_contest_detail( request , pk ):
    from .contest_status import get_contest_status
    from datetime import datetime
    contest = get_object_or_None( Contest , pk = pk )
    if not check_contest_has_perms( contest , request.user ):
        raise Http404( 'Page not found' )
    return render( request , 'contest/contest_detail.html' , {
        'contest' : contest,
        'problem_num' : range( len(contest.contestproblem_set.all()) ),
        'now' : datetime.now(),
        'conteststatus' : get_contest_status( contest.start_time , contest.end_time ) })


def get_contest_rank( request , pk ):
    from submission.models import Submission
    from .util import ContestProblemAnalysis, time_format_hm , time_format_hms
    from datetime import timedelta
    from submission.judge_result import Judge_result, get_judge_result, Query_field
    from user.models import Userinfo
    from copy import deepcopy
    from user.models import User

    contest = get_object_or_None( Contest , pk = pk )
    if not check_contest_started_or_has_perms( contest , request.user ):
        return render( request , 'contest/contest_not_started.html' )
    start_time = contest.start_time
    pos_hashtable = { x.problem : i for i , x in enumerate(contest.contestproblem_set.all()) }
    sub_all = Submission.objects.raw( 'SELECT submission_id, judge_status, submit_time, problem_id , user_id from submission_submission where contest_id = %d ORDER BY submission_id' % ( pk ) )
    user_list = { x.user_id for x in sub_all }
    user_list = { x : User.objects.get( pk = x ) for x in user_list }
    base = [ ContestProblemAnalysis(
        solved = False,
        try_times = 0,
        penalty = timedelta(),
        first_solve_timedelta = timedelta(),
        firstblood = False
    ) for i , x in enumerate( range( len( pos_hashtable ) ) ) ]
    first_blood_set = set()
    analy = dict()
    for each in sub_all:
        each.user = user_list[each.user_id]
        _id = each.problem_id
        if _id in pos_hashtable:
            se = get_judge_result( each.judge_status )
            if se not in Query_field.contest_field.value:
                continue
            user = each.user
            if user.has_perm( 'contest.hide_submission' ):
                continue
            if user not in analy:
                analy[user] = deepcopy( base )
            ts = analy[user]
            _id = pos_hashtable[_id]
            if ts[_id].solved:
                continue
            ts[_id].try_times += 1
            if se is Judge_result.AC:
                ts[_id].penalty += each.submit_time - start_time
                ts[_id].first_solve_timedelta = time_format_hm(each.submit_time - start_time)
                ts[_id].penalty += timedelta( minutes = 20 * ( ts[_id].try_times - 1 ) )
                ts[_id].solved = True
                if _id not in first_blood_set:
                    ts[_id].firstblood = True
                    first_blood_set.add( _id )
    rank = list()
    for each_user in analy:
        solvenum = 0
        ts = analy[each_user]
        all_penalty = timedelta()
        for x in ts:
            if x.solved:
                solvenum += 1
                all_penalty += x.penalty
        rank.append({
            'user' : each_user,
            'analysis' : ts,
            'solvednumber' : solvenum,
            'penalty' : all_penalty,
            'display_name' : each_user.display_name
        })
    rank.sort( key = lambda x : ( - x['solvednumber'] , x['penalty'] , x['display_name'] ) )
    for each in rank:
        each['penalty'] = time_format_hms( each['penalty'] )
    return render( request , 'contest/contest_rank.html' , {
        'contest' : contest,
        'problem_num' : range( len( pos_hashtable ) ),
        'rank' : rank,})