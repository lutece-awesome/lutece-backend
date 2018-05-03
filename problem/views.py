from django.shortcuts import get_object_or_404, render
from django.http import Http404
from django.http import HttpResponse
from .models import Problem
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import permission_required
from .validator import check_title, check_timelimit, check_memorylimit
from json import dumps

def problem_detail_view(request, problem_id):
    try:
        prob = get_object_or_404(Problem, problem_id=problem_id)
        return render(request, 'problem/problem_detail.html', {
            'prob' : prob,
            'support_lang': settings.SUPPORT_LANGUAGE_LIST,
            'sample': prob.sample_set.all()
            })
    except:
        raise Http404


def problem_list_view(request, page):
    problem_list = Problem.objects.all()
    paginator = Paginator(problem_list, settings.PER_PAGE_COUNT)
    problems = paginator.get_page(page)
    page = min( max( 1 , page ) , paginator.num_pages )
    return render(request, 'problem/problem_list.html', {
        'problist': problems,
        'max_page': paginator.num_pages,
        'page_list' : range( max( 1 , page - settings.PER_PAGINATOR_COUNT ) , min( page + settings.PER_PAGINATOR_COUNT , paginator.num_pages + 1 ) )
    })

@permission_required( 'problem.change_problem' )
def problem_edit_view( request , problem_id ):
    prob = get_object_or_404(Problem, problem_id=problem_id)
    return render( request , 'problem/problem_edit.html',{
        'prob' : prob,
        'checker' : settings.CHECKER_LIST })

@permission_required( 'problem.change_problem' )
def problem_update_view( request , problem_id ):
    status = {
        'update_status' : False,
        'error_list': []}
    err = status['error_list']
    try:
        title = request.POST.get('title')
        timelimit = request.POST.get( 'timelimit' )
        memorylimit = request.POST.get( 'memorylimit' )
        checker = request.POST.get( 'checker' )
        visible = request.POST.get( 'visible' )
        content = request.POST.get('content')
        standard_input = request.POST.get('standard_input')
        standard_output = request.POST.get('standard_output')
        constraints = request.POST.get('constraints')
        resource = request.POST.get('resource')
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


@permission_required( 'problem.add_problem' )
def problem_create_view( request ):
    
    pass