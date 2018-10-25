from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from submission.models import Submission, SubmissionCase
from graphql_jwt.shortcuts import get_user_by_token
from django.contrib.auth.models import AnonymousUser
from judge.language import Language
from judge.result import JudgeResult
from channels.db import database_sync_to_async
from json import dumps
from django.db import connections

class SubmissionDetailConsumer( AsyncWebsocketConsumer ):

	def close_old_connections( self ):
    		for conn in connections.all():
    				conn.close_if_unusable_or_obsolete()

	async def connect( self ):
<<<<<<< HEAD
		self.close_old_connections()
=======
		close_old_connections()
>>>>>>> 9a3510a8a6b62c097b04876c35a99faa53310f11
		self.submission = Submission.objects.get( pk = self.scope['url_route']['kwargs']['pk'] )
		self.group_name = f'SubmissionDetail-{self.submission.pk}'
		try:
			self.user = await database_sync_to_async(get_user_by_token)(token=self.scope['query_string'])
		except:
			self.user = AnonymousUser()
		if not self.user.has_perm('problem.view') and self.submission.problem.disable:
			raise RuntimeError('Permission Denied')
		await self.channel_layer.group_add(
			self.group_name,
			self.channel_name
		)
		await self.accept()
		await self.init()
		if self.submission.result.done:
			await self.close()

	async def init(self):
		cases = await database_sync_to_async( SubmissionCase.objects.filter )( submission = self.submission )
		lang = self.submission.language
		await self.update_result(event={'data': {
		    'result': self.submission.result.result.full,
		    'judge':  [each.get_websocket_field() for each in cases],
		    'compileerror_msg': self.submission.result.compile_info,
		    'judgererror_msg': self.submission.result.error_info,
		    'code': self.submission.code,
		    'casenumber': self.submission.attach_info.cases_count,
		    'codehighlight': lang.codemirror,
		    'completed': self.submission.result.done,
		    'problem__title': self.submission.problem.title,
		    'problem__slug': self.submission.problem.slug,
		    'user__username': self.submission.user.username,
		    'submit_time': self.submission.create_time.strftime("%Y-%m-%d %H:%M:%S"),
		}})

	async def disconnect(self, close_code):
		await self.channel_layer.group_discard(
		    self.group_name,
		    self.channel_name
		)

	async def update_result(self, event):
		data = event['data']
		perm = self.submission.user == self.user
		privilege = self.user.has_perm('submission.view')
		if 'compileerror_msg' in data and not (perm or privilege):
		    data.pop('compileerror_msg')
		if 'judgererror_msg' in data and not privilege:
		    data.pop('judgererror_msg')
		if 'code' in data and not (perm or privilege):
		    data.pop('code')
		if 'result' in data:
		    data['result_color'] = JudgeResult.value_of( data['result'] ).color
		await self.send(text_data=dumps(data))