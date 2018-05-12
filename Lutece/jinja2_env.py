from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse

from jinja2 import Environment
from django_gravatar.helpers import get_gravatar_url


def environment(**options):
    env = Environment(**options)
    from submission.judge_result import get_judge_result_color, get_judge_result_icon , check_judge_result_in_listshow_field
    env.filters['get_judge_result_color'] = get_judge_result_color
    env.filters['get_judge_result_icon'] = get_judge_result_icon
    env.filters['check_judge_result_in_listshow_field'] = check_judge_result_in_listshow_field
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
        'gravatar_url': get_gravatar_url
    })
    return env