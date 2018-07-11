from django.shortcuts import render, get_object_or_404
from .models import User
from .group import Group
from django.http import HttpResponse, QueryDict
from django.contrib.auth import authenticate, login, logout
from json import dumps
from annoying.functions import get_object_or_None
from django.contrib.auth.decorators import login_required
from .util import get_recently, get_user_report
from submission import judge_result
from Lutece.config import RECENT_NUMBER
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from utils.paginator_menu import get_range as page_range
import Lutece.config as config
from django.urls import reverse


def user_login( request ):
    status = {
        'login_status': False}
    username = request.POST.get('username')
    password = request.POST.get('password')
    login_user = get_object_or_None( User , username = username )
    if login_user and login_user.check_password( password ):
        login(request, login_user)
        status['login_status'] = True
    return HttpResponse(dumps(status), content_type='application/json')


def user_logout(request):
    status = {
        'logout_status': True}
    logout(request)
    return HttpResponse(dumps(status), content_type='application/json')


def user_signup(request):
    status = {
        'signup_status': False,
        'error_msg': ''}
    from .form import UserSignupForm
    SignupForm = UserSignupForm( request.POST )
    if SignupForm.is_valid():
        values = SignupForm.cleaned_data
        new_user = User(
            username = values['username'],
            email = values['email'],
            display_name = values['displayname'],
            is_staff = False,
            is_superuser = False,)
        new_user.set_password( values['password'] )
        new_user.save()
        new_user.set_group( Group.NORMAL_USER )
        login( request , new_user )
        status['signup_status'] = True
    else:
        status['error_msg'] = SignupForm.errors.as_ul()
    return HttpResponse( dumps( status ) , content_type = 'application/json' )

@login_required
def user_infomodify( request ):
    status = {
        'status': False,
        'error_msg': ''}
    from .form import UserinfoForm
    InfoForm = UserinfoForm( request.POST )
    oridisplay_name = request.user.display_name
    print( oridisplay_name )
    if InfoForm.is_valid() and InfoForm._clean( oridisplay_name ):
        values = InfoForm.cleaned_data
        request.user.about = values['about']
        request.user.school = values['school']
        request.user.company = values['company']
        request.user.location = values['location']
        request.user.display_name = values['displayname']
        request.user.save()
        status['status'] = True
    else:
        status['error_msg'] = InfoForm.errors.as_ul()
    return HttpResponse( dumps( status ) , content_type = 'application/json' )

def user_detail( request , user_id ):
    target_user = get_object_or_404( User , pk = user_id )
    return render( request , 'user/user_detail.html' , {
        'target_user' : target_user,
        ** get_user_report( user = target_user , has_perm = request.user.has_perm( 'problem.view_all' ) ),
        'recently' : get_recently( user = target_user , number = RECENT_NUMBER , has_perm = request.user.has_perm( 'problem.view_all' ) ) })

def user_search( request , displayname ):
    ret = User.objects.filter(display_name__contains = displayname)[:5]
    return HttpResponse(dumps( { 'items' : [ { 'title': x.display_name , 'html_url' : reverse( 'user-detail' , args = ( x.pk, ) ) } for x in ret ] } ), content_type='application/json')

def user_list( request , page ):
    paginator = Paginator( User.objects.filter( show = True ).order_by( '-solved' ) , config.USER_PER_PAGE_COUNT )
    page = min( max( 1 , page ) , paginator.num_pages )
    user_list = paginator.get_page( page )
    return render( request , 'user/user_list.html' ,{
        'user_list' : user_list,
        'currentpage' : page,
        'max_page': paginator.num_pages,
        'page_list' : page_range( page , paginator.num_pages )} )

@login_required
def toggle_follow_realtion( request , user_id ):
    status = { 'status' : False, }
    target = User.objects.get( pk = user_id )
    try:
        if request.user == target:
            raise TypeError( 'Can not follow self' )
    finally:
        return HttpResponse( dumps( status ) , content_type = 'application/json' )