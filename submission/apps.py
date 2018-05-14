from django.apps import AppConfig
from django.db.models.signals import pre_save

class SubmissionConfig(AppConfig):
    name = 'submission'
    def ready( self ):
        pass