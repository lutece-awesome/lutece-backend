from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
<<<<<<< HEAD
from .models import Submission, Judgeinfo
from json import dumps
from .util import construct_websocketdata

class StatusDetailConsumer( WebsocketConsumer ):

    async def connect( self ):
        self.submission = Submission.objects.get( self.scope['url_route']['kwargs']['pk'] )
        self.group_name = 'StatusDetail_%d' % self.submission.pk
        '''
            Auth
        '''
        if not self.scope['user'].has_perm( 'problem.view_all' ) and not self.submission.problem.visible:
            raise RuntimeError( 'Permission Denied' )

        await async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        await self.accept()
        self.init()

    '''
        Send the judge_result that has been created before
    '''

    async def init( self ):
        s = Judgeinfo.objects.filter( submission = self.submission )
        self.send( text_data = construct_websocketdata( result = self.submission.judge_status ,  judge =  [ {
            'timecost' : each.time_csot,
            'memorycost' : each.memory_cost,
            'result': each.result,
            'case': each.case
        } for each in s ] ) )
    
    async def disconnect( self , close_code ):
        await async_to_sync(self.channel_layer.group_discard)(
=======
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
>>>>>>> 6e2fa91ac96994be179bd4031e5cd299499fbbf0
            self.group_name,
            self.channel_name
        )

<<<<<<< HEAD
    async def update_result( self , event ):
        data = event['data']
        self.send( text_data = data )
=======
    def initialize( self ):
        if not self.init:
            self.init = True

    def update_result( self , message ):
        pass
>>>>>>> 6e2fa91ac96994be179bd4031e5cd299499fbbf0
