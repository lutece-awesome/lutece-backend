from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Contest
from Lutece import config
from utils.paginator_menu import get_range as page_range

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
        'page_list' : page_range( page , paginator.num_pages ) })


@permission_required( 'contest.add_contest' )
def create_contest( request ):
    pass