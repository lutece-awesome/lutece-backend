from django.conf.urls import url
from submission.consumers import SubmissionDetailConsumer

websocket_urlpatterns = [
    url( r'ws/status/(?P<pk>\d{1,})/$' , SubmissionDetailConsumer )
]