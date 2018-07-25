from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Submission, Judgeinfo
from graphql_jwt.shortcuts import get_user_by_token
from django.contrib.auth.models import AnonymousUser
from utils.language import Language
from json import dumps
from submission.judge_result import get_judge_result_color
from channels.db import database_sync_to_async


class StatusDetailConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.submission = Submission.objects.get(
            pk=self.scope['url_route']['kwargs']['pk'])
        self.group_name = 'StatusDetail_%d' % self.submission.pk
        try:
            self.user = await database_sync_to_async(get_user_by_token)(token=self.scope['query_string'])
        except:
            self.user = AnonymousUser()
        '''
            Auth
        '''
        if not self.user.has_perm('problem.view_all') and not self.submission.problem.visible:
            raise RuntimeError('Permission Denied')
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

    async def init(self):
        s = await database_sync_to_async(Judgeinfo.objects.filter)(submission=self.submission)
        lang = Language.get_language(self.submission.language)
        await self.update_result(event={'data': {
            'result': self.submission.judge_status,
            'judge':  [each.get_websocket_field() for each in s],
            'compileerror_msg': self.submission.compileerror_msg,
            'judgererror_msg': self.submission.judgererror_msg,
            'completed': self.submission.completed,
            'code': self.submission.code,
            'casenumber': self.submission.case_number,
            'codehighlight': lang.value.codemirror,
            'completed': self.submission.completed,
            'problem__title': self.submission.problem.title,
            'problem__slug': self.submission.problem.slug,
            'user__display_name': self.submission.user.display_name,
            'user__username': self.submission.user.username,
            'submit_time': self.submission.submit_time.strftime("%Y-%m-%d %H:%M:%S"),
        }})

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def update_result(self, event):
        data = event['data']
        perm = self.submission.user == self.user
        privilege = self.user.has_perm('submission.view_all')
        if 'compileerror_msg' in data and not (perm or privilege):
            data.pop('compileerror_msg')
        if 'judgererror_msg' in data and not privilege:
            data.pop('judgererror_msg')
        if 'code' in data and not (perm or privilege):
            data.pop('code')
        if 'result' in data:
            data['result_color'] = get_judge_result_color(data['result'])
        await self.send(text_data=dumps(data))
