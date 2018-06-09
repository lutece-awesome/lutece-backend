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
        'now' : datetime.now(),
        'conteststatus' : get_contest_status( contest.start_time , contest.end_time ),
        'contesttype' : get_contest_type( contest.contest_type ),
    })


def get_contest_problem( request , pk , index ):
    from problem.models import Problem
    from utils.language import get_language_list
    contest = get_object_or_None( Contest, pk = pk )
    prob = get_object_or_None( Problem , pk = contest.contestproblem_set.all()[index].problem )
    return render( request , 'contest/contest_problem.html' ,{
        'prob' : prob,
        'support_lang': get_language_list(),
        'sample': prob.sample_set.all(),
        'contest' : contest,
        'conteststatus' : get_contest_status( contest.start_time , contest.end_time ),
        'now' : datetime.now(),
    })

def get_problem_list( request , pk ):
    from problem.models import Problem
    contest = get_object_or_None( Contest , pk = pk )
    return render( request , 'contest/contest_problem_list.html' , {
        'contest' : contest,
        'now' : datetime.now(),
        'conteststatus' : get_contest_status( contest.start_time , contest.end_time ),
        'prob' : [ get_object_or_None( Problem , pk = x.problem ) for x in contest.contestproblem_set.all() ],
    })
