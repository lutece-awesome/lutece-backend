from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse

from jinja2 import Environment
from django_gravatar.helpers import get_gravatar_url


def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
        'gravatar_url': get_gravatar_url
    })
    return env