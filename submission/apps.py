from django.apps import AppConfig
from django.db.models.signals import pre_save
from .tasks import init_push_waiting_submission

class SubmissionConfig(AppConfig):
    name = 'submission'
    def ready( self ):
        init_push_waiting_submission()
