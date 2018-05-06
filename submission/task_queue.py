from Lutece.settings import JUDGE_AUTH_KEY, JUDGE_PORT
from multiprocessing.managers import BaseManager
import queue

class QueueManager(BaseManager):
    pass

task_queue = queue.Queue()
result_queue = queue.Queue()
QueueManager.register('get_task_queue', callable=lambda: task_queue)
QueueManager.register('get_result_queue', callable=lambda: result_queue)
manager = QueueManager( address=('127.0.0.1', JUDGE_PORT), authkey = JUDGE_AUTH_KEY )
manager.start()
task = manager.get_task_queue()
result = manager.get_result_queue()