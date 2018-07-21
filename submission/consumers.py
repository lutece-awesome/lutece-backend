from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
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
            self.group_name,
            self.channel_name
        )

    async def update_result( self , event ):
        data = event['data']
        self.send( text_data = data )