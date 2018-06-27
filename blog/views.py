from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from json import dumps
from .models import Blog
# Create your views here.


@login_required
def create( request ):
    status = {
        'status' : True,
        'error' : ''}
    from .form import BlogBasicForm
    user = request.user
    Blogform = BlogBasicForm( request.POST )
    if Blogform.is_valid():
        values = Blogform.cleaned_data
        title = values['title']
        content = values['content']
        Blog(
            title = title,
            content = content,
            user = request.user).save()
    else:
        status['error'] = Blogform.errors
    return HttpResponse(dumps(status), content_type='application/json')