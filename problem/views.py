from django.shortcuts import get_object_or_404, render
from django.http import Http404
from django.http import HttpResponse
from .models import Problem
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def problem_detail_view(request, problem_id):
    prob = get_object_or_404(Problem, problem_id=problem_id)
    return render(request, 'problem/problem_detail.html', {
        'prob' : prob,
        'support_lang': settings.SUPPORT_LANGUAGE_LIST,
        })


def problem_list_view(request, page):
    problem_list = Problem.objects.all()
    paginator = Paginator(problem_list, settings.PER_PAGE_COUNT)
    try:
        problems = paginator.page(page)
    except EmptyPage:
        problems = paginator.page(paginator.num_pages)
    return render(request, 'problem/problem_list.html', {'problist': problems,})
