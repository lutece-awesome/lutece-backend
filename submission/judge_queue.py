from Lutece.settings import JUDGE_AUTH_KEY, JUDGE_PORT
from multiprocessing.managers import BaseManager
import queue
from sys import modules

class QueueManager(BaseManager):
    pass

class _JudgeQueue:

    def __init__( self ):
        task_queue = queue.Queue()
        result_queue = queue.Queue()
        QueueManager.register('get_task_queue', callable=lambda: task_queue)
        QueueManager.register('get_result_queue', callable=lambda: result_queue)
        manager = QueueManager( address=('127.0.0.1', JUDGE_PORT), authkey = JUDGE_AUTH_KEY )
        manager.start()
        self.task = manager.get_task_queue()
        self.result = manager.get_result_queue()

modules[__name__] = _JudgeQueue()