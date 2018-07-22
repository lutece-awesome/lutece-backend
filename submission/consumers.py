from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Submission, Judgeinfo
from .util import construct_websocketdata
from graphql_jwt.shortcuts import get_user_by_token
from django.contrib.auth.models import AnonymousUser

class StatusDetailConsumer( AsyncWebsocketConsumer ):

    async def connect( self ):
        self.submission = Submission.objects.get( pk = self.scope['url_route']['kwargs']['pk'] )
        self.group_name = 'StatusDetail_%d' % self.submission.pk
        try:
            self.user = get_user_by_token( token = self.scope['query_string'] )
        except:
            self.user = AnonymousUser()
        print( self.user )
        '''
            Auth
        '''
        if not self.user.has_perm( 'problem.view_all' ) and not self.submission.problem.visible:
            raise RuntimeError( 'Permission Denied' )
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()
        await self.init()
        if self.submission.completed:
            await self.close()

    '''
        Send the judge_result that has been created before
    '''

    async def init( self ):
        s = Judgeinfo.objects.filter( submission = self.submission )
        await self.send( text_data = construct_websocketdata( result = self.submission.judge_status ,  judge =  [ {
            'timecost' : each.time_cost,
            'memorycost' : each.memory_cost,
            'result': each.result,
            'case': each.case
        } for each in s ] ) )
    
    async def disconnect( self , close_code ):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def update_result( self , event ):
        data = event['data']
        await self.send( text_data = data )
