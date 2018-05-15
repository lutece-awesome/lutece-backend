from multiprocessing.managers import BaseManager
from Lutece.production import JUDGE_AUTH_KEY, JUDGE_PORT
from sys import modules
from queue import Queue
from threading import Thread
import signal

class QueueManager(BaseManager):
    pass

class _manager:

    def __init__( self ):
        task_queue = Queue()
        result_queue = Queue()
        QueueManager.register('get_task_queue', callable=lambda: task_queue)
        QueueManager.register('get_result_queue', callable=lambda: result_queue)
        self.m = QueueManager(address=('0.0.0.0', JUDGE_PORT ), authkey = JUDGE_AUTH_KEY )
        s = self.m.get_server()
        s.serve_forever()
        #self.m.start( signal.signal, (signal.SIGINT, signal.SIG_IGN) )

modules[__name__] = _manager()