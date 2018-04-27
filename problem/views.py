from django.shortcuts import get_object_or_404, render
from django.http import Http404
from django.http import HttpResponse
from .models import Problem
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def problem_detail_view(request, problem_id):
    try:
        prob = get_object_or_404(Problem, problem_id=problem_id)
        print(prob.sample_set.all() )
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
