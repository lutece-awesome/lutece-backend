from django.shortcuts import render

# Create your views here.

def home_render( request ):
    from user.models import User
    top_user = User.objects.filter( show = True ).order_by( '-solved' )[:10]
    return render( request , 'home/home.html' , {
        'top_user' : top_user,
    } )
