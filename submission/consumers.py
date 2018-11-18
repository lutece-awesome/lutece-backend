from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser
from graphql_jwt.shortcuts import get_user_by_token
from humps import camelize
from json import dumps
from typing import List

from submission.models import Submission, SubmissionCase
from user.models import User
from utils.function import close_old_connections


class CaseData:
    __slots__ = {
        'result',  # type: str
        'time_cost',  # type: int
        'memory_cost',  # type: int
        'case',  # type: int
    }

    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            if key in self.__slots__:
                setattr(self, key, value)

    def serialization(self):
        return {camelize(each): getattr(self, each) for each in self.__slots__}


class UpdatingData:
    __slots__ = {
        'result',  # type: str
        'code',  # type: str
        'case_number',  # type: int
        'submit_time',  # type: str
        'language',  # type: str
        'compile_info',  # type: str
        'error_info',  # type: str
        'problem_title',  # type: str
        'problem_slug',  # type: str
        'submit_user',  # type: str
        'case_list',  # type: List[UpdatingData]
    }

    def filter(self, filter_data: List[str]):
        for each in filter_data:
            if hasattr(self, each):
                setattr(self, each, None)

    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            if key in self.__slots__:
                setattr(self, key, value)


class SubmissionDetailConsumer(AsyncWebsocketConsumer):
    __slots__ = {
        'submission',  # type: Submission
        'group_name',  # type: str
        'user',  # type: User
    }

    async def connect(self):
        close_old_connections()
        self.submission = Submission.objects.get(pk=self.scope['url_route']['kwargs']['pk'])
        self.group_name = f'SubmissionDetail-{self.submission.pk}'
        try:
            self.user = await database_sync_to_async(get_user_by_token)(token=self.scope['query_string'])
        except Exception:
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
        cases = await database_sync_to_async(SubmissionCase.objects.filter)(submission=self.submission)
        await self.update_result(
            event={
                'data': UpdatingData(
                    result=self.submission.result.result.full,
                    code=self.submission.code,
                    case_number=self.submission.attach_info.cases_count,
                    submit_time=self.submission.create_time.strftime("%Y-%m-%d %H:%M:%S"),
                    language=self.submission.language.full,
                    compile_info=self.submission.result.compile_info,
                    error_info=self.submission.result.error_info,
                    problem_title=self.submission.problem.title,
                    problem_slug=self.submission.problem.slug,
                    submit_user=self.submission.user.username,
                    case_list=[CaseData(
                        result=each.result.full,
                        time_cost=each.time_cost,
                        memory_cost=each.memory_cost,
                        case=each.case
                    ) for each in cases]
                )
            }
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def update_result(self, event: dict):
        data = event.get('data')
        perm = self.submission.user == self.user
        privilege = self.user.has_perm('submission.view')
        if not (perm or privilege):
            data.filter(['compile_info', 'code'])
        if not privilege:
            data.filter(['error_info'])
        setattr(data, 'case_list', [each.serialization() for each in getattr(data, 'case_list')])
        ret = dict()
        for each in data.__slots__:
            if hasattr(data, each):
                val = getattr(data, each)
                if val:
                    ret[camelize(each)] = val

        await self.send(text_data=dumps(ret))
