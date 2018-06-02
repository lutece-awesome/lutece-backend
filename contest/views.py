from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Contest
from Lutece import config
from utils.paginator_menu import get_range as page_range
from .contest_type import get_contest_type_list, get_contest_type
from django.http import HttpResponse
from json import dumps
from annoying.functions import get_object_or_None

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