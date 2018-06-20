from django.shortcuts import render
from .models import Discussion
from django.http import Http404


def show_discussions(request, pk):
    discussion = Discussion.objects.get(
        discussion_id=pk)
    if not discussion.visibility:
        raise Http404( 'Permission Denied')
    return render(request, 'discussion/discussion.html', {
        'discussion': discussion, })
