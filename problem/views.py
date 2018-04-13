from django.shortcuts import get_object_or_404, render
from django.http import Http404
from django.http import HttpResponse
from .models import Problem
from Config import config


def problem_view(request, problem_id):
    prob = get_object_or_404(Problem, problem_id=problem_id)
    context = {'prob': prob.toDict()}
    return render(request, 'problem/problemView.html', context)


def problem_list(request, page):
    p = Problem.objects.raw('SELECT problem_id , title , try_number, solved_number FROM problem_problem WHERE problem_id BETWEEN {rangel} and {ranger} ORDER BY problem_id ASC'.format(
        rangel=(page - 1) * config.perPagecount + 1,
        ranger=page * config.perPagecount
    ))
    return render(request, 'problem/problemList.html', {'problist': p})
