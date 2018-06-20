from django.shortcuts import get_object_or_404, render
from django.http import Http404
from django.http import HttpResponse
from .models import Problem, Sample
from django.conf import settings
import Lutece.config as config
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import permission_required
from .validator import check_title, check_timelimit, check_memorylimit
from .util import get_problem_analysis , get_user_problem_analysis, check_visible_permission_or_404
from utils.paginator_menu import get_range as page_range
from utils.language import get_language_list
from json import dumps, loads
from data_server.util import get_case_number, make_data_folder
from django.views.decorators.csrf import csrf_exempt
from data_server.util import upload_data
from annoying.functions import get_object_or_None
from django.urls import reverse

def problem_detail(request, problem_id):
    prob = get_object_or_404(Problem, problem_id=problem_id)
    check_visible_permission_or_404( user = request.user , problem = prob )
    return render(request, 'problem/problem_detail.html', {
        'prob' : prob,
        'support_lang': get_language_list(),
        'sample': prob.sample_set.all()})

def problem_list(request, page):
    problem_list = Problem.objects.all()
    if not request.user.has_perm( 'problem.view_all' ):
        problem_list = problem_list.filter( visible = True )
    paginator = Paginator(problem_list, config.PER_PAGE_COUNT)
    problems = paginator.get_page(page)
    page = min( max( 1 , page ) , paginator.num_pages )
    user_analysis = None
    if request.user.is_authenticated:
        user_analysis = [ get_user_problem_analysis( user = request.user , problem = x ) for x in problems ]
    return render(request, 'problem/problem_list.html', {
        'problist': problems,
        'currentpage' : page,
        'user_analysis' : user_analysis,
        'max_page': paginator.num_pages,
        'page_list' : page_range( page , paginator.num_pages ) })

@permission_required( 'problem.change_problem' )
def problem_edit( request , problem_id ):
    prob = get_object_or_404(Problem, problem_id=problem_id)
    return render( request , 'problem/problem_edit.html',{
        'prob' : prob,
        'case_number' : get_case_number( problem_id ),
        'sample': prob.sample_set.all(),
        'checker' : config.CHECKER_LIST })

@permission_required( 'problem.change_problem')
@csrf_exempt
def problem_upload_data( request , problem_id ):
    status = {'error_list': []}
    data = request.FILES['data']
    status['status'] = upload_data( 
        data = data ,
        problem = problem_id,
        errlist = status['error_list'])
    if status['status'] is True:
        status['case_number'] = get_case_number( problem_id ) 
    return HttpResponse(dumps(status), content_type='application/json')

@permission_required( 'problem.change_problem' )
def problem_update( request , problem_id ):
    status = {
        'update_status' : False,
        'error_list': []}
    err = status['error_list']
    try:
        title = request.POST.get('title').strip()
        timelimit = request.POST.get( 'timelimit' )
        memorylimit = request.POST.get( 'memorylimit' )
        checker = request.POST.get( 'checker' )
        visible = request.POST.get( 'visible' )
        content = request.POST.get('content')
        note = request.POST.get( 'note' )
        standard_input = request.POST.get('standard_input')
        standard_output = request.POST.get('standard_output')
        constraints = request.POST.get('constraints')
        resource = request.POST.get('resource')
        sample = loads(request.POST.get( 'sample' ))
        prob = Problem.objects.get( pk = problem_id )
        prob.sample_set.all().delete()
        for x in sample:
            Sample(
                input_content = x[0],
                output_content = x[1],
                problem = prob
            ).save()
        check_title( title , err )
        check_timelimit( timelimit , err )
        check_memorylimit( memorylimit , err )
        if len( err ) > 0:
            raise ValueError( "Some Update field wrong" )
        Problem.objects.filter( problem_id = problem_id ).update( 
            title = title,
            time_limit = int( timelimit ),
            memory_limit = int( memorylimit ),
            checker = checker,
            visible = True if visible == 'true' else False,
            content = content,
            note = note,
            standard_input = standard_input,
            standard_output = standard_output,
            constraints = constraints,
            resource = resource)
        status['update_status'] = True
    except Exception as e:
        err.append( str( e ) )
        err.reverse()
    finally:
        return HttpResponse(dumps(status), content_type='application/json')

def search( request , til ):
    _all = Problem.objects.all()
    if not request.user.has_perm( 'problem.view_all' ):
        _all = _all.filter( visible = True )
    ret = _all.filter(title__contains=til)[:5]
    return HttpResponse(dumps( { 'items' : [ { 'title': x.title , 'html_url' : reverse( 'problem-detail' , args = (x.pk ,) ) } for x in ret ] } ), content_type='application/json')

@permission_required( 'problem.add_problem' )
def problem_create_check( request ):
    status = {
        'status' : False,
        'error_list': []}
    err = status['error_list']
    try:
        title = request.POST.get( 'title' ).strip()
        if not check_title( title , err ):
            return
        if get_object_or_None( Problem , title = title ) is not None:
            err.append( 'Title should be unique' )
            return
        s = Problem( title = title )
        s.save()
        status['problem_id'] = s.pk
        make_data_folder( s.pk )
        if len( err ) == 0:
            status['status'] = True
    except Exception as Error:
        err.append( str( Error ) )
    finally:
        return HttpResponse(dumps(status), content_type='application/json')

def query_title( request , pk ):
    status = {
        'status' : False,}
    s = get_object_or_None( Problem , pk = pk )
    if s is not None:
        status['status'] = True
        status['title'] = s.title
    return HttpResponse(dumps(status), content_type='application/json')