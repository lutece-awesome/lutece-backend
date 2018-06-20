from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse

from jinja2 import Environment,evalcontextfilter, Markup, escape
from django_gravatar.helpers import get_gravatar_url
from django.contrib.humanize.templatetags.humanize import naturaltime
import re


_paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')
 
@evalcontextfilter
def nl2br(eval_ctx, value):
    result = u'\n\n'.join(u'<p>%s</p>' % p.replace('\n', Markup('<br>\n'))
                          for p in _paragraph_re.split(escape(value)))
    if eval_ctx.autoescape:
        result = Markup(result)
    return result

def register_judge_result( env ):
    from submission.judge_result import get_judge_result_color, get_judge_result_icon , check_judge_result_in_listshow_field, is_compile_error, is_judger_error, get_CE_JE_info
    env.filters['get_judge_result_color'] = get_judge_result_color
    env.filters['get_judge_result_icon'] = get_judge_result_icon
    env.filters['check_judge_result_in_listshow_field'] = check_judge_result_in_listshow_field
    env.filters['is_compile_error'] = is_compile_error
    env.filters['is_judger_error'] = is_judger_error
    env.filters['get_CE_JE_info'] = get_CE_JE_info

def register_language( env ):
    from utils.language import get_prism
    env.filters['get_prism'] = get_prism

def append_query_parameters( url , query ):
    return url + '?' + query if len( query ) else url

def get_user_group( user ):
    from user.group import get_user_group
    return get_user_group( user.group )

def register_user(env):
    from user.group import get_user_control_permission
    env.filters['get_user_group'] = get_user_group
    env.filters['get_user_control_permission'] = get_user_control_permission

def timedeltaformat( s ):
    days = s.days
    seconds = s.seconds
    hours = seconds // 3600
    seconds = seconds % 3600
    mins = seconds // 60
    seconds = seconds % 60
    last = '%.2d:%.2d:%.2d' % ( hours, mins, seconds )
    if days > 0:
        last = '{days} days '.format(
            days = days
        ) + last
    return last

def I2S( it ):
    return chr( it + ord('A') )

def environment(**options):
    env = Environment(**options)
    env.filters['nl2br'] = nl2br
    register_judge_result( env )
    register_language( env )
    register_user( env )
    env.filters['append_query_parameters'] = append_query_parameters
    env.filters['timedeltaformat'] = timedeltaformat
    env.filters['I2S'] = I2S
    env.filters['naturaltime'] = naturaltime
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
        'gravatar_url': get_gravatar_url,
    })
    return env