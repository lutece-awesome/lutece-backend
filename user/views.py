from django.shortcuts import render, get_object_or_404
from .models import User, Group, Userinfo
from django.http import HttpResponse, QueryDict
from django.contrib.auth import authenticate, login, logout
from json import dumps
from .user_signup.password_checker import get_password_strength
from .user_signup.email_checker import get_email_report
from .user_signup.username_checker import get_username_strength
from annoying.functions import get_object_or_None
from django.contrib.auth.decorators import login_required
from .util import get_recently
from submission import judge_result
from Lutece.config import RECENT_NUMBER
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from utils.paginator_menu import get_range as page_range
import Lutece.config as config
from django.urls import reverse


def user_login(request):
    status = {
        'login_status': False}
    try:
        if request.method == 'POST':
            username = request.POST.get('username').strip()
            password = request.POST.get('password')
            if username == None or password == None:
                raise ValueError("username or password do not exist")
            login_user = get_object_or_None( User , username = username )
            if login_user == None:
                raise ValueError("user not exist")
            if login_user.check_password(password):
                login(request, login_user)
                status['login_status'] = True
    except Exception as e:
        print( 'Error on user_login' , str( e ) )
    finally:
        return HttpResponse(dumps(status), content_type='application/json')


def user_logout(request):
    status = {
        'logout_status': True}
    logout(request)
    return HttpResponse(dumps(status), content_type='application/json')


def user_signup(request):
    status = {
        'signup_status': False,
        'error_msg': []}
    errormsg_list = status['error_msg']
    try:
        if request.method == 'POST':
            username = request.POST.get('username').strip()
            password = request.POST.get('password')
            email = request.POST.get('email').strip()
            displayname = request.POST.get('displayname').strip()
            if username == None or password == None or email == None or displayname == None:
                raise ValueError( "Some sign up info do not exist." )
            # Check username
            if len( username ) > 0:
                login_user = get_object_or_None( User,
                    username = username)
                if login_user != None:
                    errormsg_list.append('Username already exists.')
                else:
                    usr_report = get_username_strength( username )
                    if len( usr_report ) > 0:
                        errormsg_list.append( usr_report )
            else:
                errormsg_list.append( 'Username can not be empty.' )
            # Check password
            if len( password ) > 0:
                pwd_check_report = get_password_strength( password )
                for _ in pwd_check_report:
                    errormsg_list.append( _ )
            else:
                errormsg_list.append( 'Password can not be empty.' )
            # Check email
            if len( email ) > 0:
                login_user = get_object_or_None( User,
                    email = email)
                if login_user != None:
                    errormsg_list.append('Email already exists.')
                else:
                    email_report = get_email_report( email )
                    if( len( email_report ) > 0 ):
                        errormsg_list.append( email_report )
            else:
                errormsg_list.append( 'Email can not be empty.' )
            # Check displayname
            if len( displayname ) == 0:
                errormsg_list.append( 'Displayname can not be empty.' )
            elif len( displayname ) > 12:
                errormsg_list.append( 'The length of displayname too long.' )
            elif get_object_or_None( User , display_name = displayname ) is not None:
                errormsg_list.append( 'Display name already exists.' )
            # Check error_msg
            if len( errormsg_list ) == 0:
                new_user = User(
                    username = username,
                    email = email,
                    display_name = displayname,
                    is_staff = False,
                    is_superuser = False,
                )
                new_user.set_password( password )
                status['signup_status'] = True
                new_user.set_group( Group.normal_user )
                new_user.save()
                login(request,new_user)
    except Exception as e:
        print( 'Error on user_signup' , str( e ) )
    finally:
        return HttpResponse( dumps( status ) , content_type = 'application/json' )

@login_required
def user_infomodify( request ):
    status = {
        'status': False,
        'error_msg': []}
    msg = status['error_msg']
    try:
        if request.method == 'POST':
            about = request.POST.get( 'about' ).strip()
            school = request.POST.get( 'school' ).strip()
            company = request.POST.get( 'company' ).strip()
            location = request.POST.get( 'location' ).strip()
            display_name = request.POST.get( 'display_name' ).strip()
            oridisplay_name = User.objects.get( id = request.user.pk ).display_name
            if len( about ) > 256:
                msg.append( 'About\'s length is too long' )
            if len( school ) > 60:
                msg.append( 'Are u sure this is a valid school?' )
            if len( company ) > 32:
                msg.append( 'Are u sure this is a valid company?' )
            if len( location ) > 32:
                msg.append( 'Are u sure this is a valid location?' )
            if len( display_name ) > 16:
                msg.append( 'Your display name too long' )
            elif len( display_name ) == 0:
                msg.append( 'Display name can not be empty' )
            if display_name != oridisplay_name and get_object_or_None( User , display_name = display_name ) is not None:
                msg.append( 'Display name already exists.' )
            if len( msg ) == 0:
                Userinfo.objects.filter( user = request.user ).update(
                    about = about,
                    school = school,
                    company = company,
                    location = location)
                User.objects.filter( id = request.user.pk ).update(
                    display_name = display_name) 
                status['status'] = True
    except Exception as e:
        print( str( e ) )
    finally:
        return HttpResponse( dumps( status ) , content_type = 'application/json' )

def user_detail( request , user_id ):
    target_user = get_object_or_404( User , pk = user_id )
    return render( request , 'user/user_detail.html' , {
        'target_user' : target_user,
        'info' : Userinfo.objects.get( user = target_user),
        ** get_user_report( user = target_user , has_perm = request.user.has_perm( 'problem.view_all' ) ),
        'recently' : get_recently( user = target_user , number = RECENT_NUMBER , has_perm = request.user.has_perm( 'problem.view_all' ) ) })

def user_search( request , displayname ):
    ret = User.objects.filter(display_name__contains = displayname)[:5]
    return HttpResponse(dumps( { 'items' : [ { 'title': x.display_name , 'html_url' : reverse( 'user-search' , args = ( x.pk, ) ) } for x in ret ] } ), content_type='application/json')

def user_list( request , page ):
    paginator = Paginator( Userinfo.objects.all().order_by( '-solved' ) , config.USER_PER_PAGE_COUNT )
    page = min( max( 1 , page ) , paginator.num_pages )
    userinfo_list = paginator.get_page( page )
    return render( request , 'user/user_list.html' ,{
        'userinfo_list' : userinfo_list,
        'currentpage' : page,
        'max_page': paginator.num_pages,
        'page_list' : page_range( page , paginator.num_pages )} )


@login_required
def toggle_follow_realtion( request , user_id ):
    status = {
        'status' : False,
    }
    target = User.objects.get( pk = user_id )
    try:
        if request.user == target:
            raise TypeError( 'Can not follow self' )
        
    finally:
        return HttpResponse( dumps( status ) , content_type = 'application/json' )