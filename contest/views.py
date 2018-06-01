from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Contest
from Lutece import config
from utils.paginator_menu import get_range as page_range
from .contest_type import get_contest_type_list

# Create your views here.



def get_contest_list( request , page ):
    contest_list = Contest.objects.all()
    if not request.user.has_perm( 'contest.view_all' ):
        contest_list = contest_list.filter( visible = True )
    paginator = Paginator(contest_list, config.PER_PAGE_COUNT)
    contests = paginator.get_page(page)
    page = min( max( 1 , page ) , paginator.num_pages )
    return render(request, 'contest/contest_list.html', {
        'contestlist': contests,
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
        check_title( title , err )
        if get_object_or_None( Contest , title = title ) is not None:
            err.append( 'Title should be unique' )
            raise TypeError( 'Title Field should unique' )
        s = Contest( title = title )
        s.save()
        status['contest_id'] = s.pk
        if len( err ) == 0:
            status['status'] = True
    finally:
        return HttpResponse(dumps(status), content_type='application/json')