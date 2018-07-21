from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import Submission


class StatusDetailConsumer( WebsocketConsumer ):

    def connect( self ):
        self.pk = self.scope['url_route']['kwargs']['pk']
        self.group_name = 'StatusDetail_%d' % self.pk
        self.init = False
        self.submission = Submission.objects.get( self.pk )

        if not self.scope['user'].has_perm( 'problem.view_all' ) and not self.submission.problem.visible:
            raise RuntimeError( 'Permission Denied' )

        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        self.accept()
    
    def disconnect( self , close_code ):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    def initialize( self ):
        if not self.init:
            self.init = True

    def update_result( self , message ):
        pass
