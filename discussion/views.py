from django.shortcuts import render
from .models import Discussion

def show_discussions(request, pk):
    return render(request, "discussion/discussion.html", {'discussions': Discussion.objects.all()})