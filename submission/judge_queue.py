from Lutece.production import JUDGE_AUTH_KEY, JUDGE_PORT
from multiprocessing.managers import BaseManager
import queue
from sys import modules
from threading import Thread
from .models import Submission, Judgeinfo

class QueueManager(BaseManager):
    pass

def get_update_dict( dic ):
    L = []
    t = dic
    for _ in t:
        if _ not in Submission.Judge.update_field:
            L.append( _ )
    for _ in L:
        t.pop( _ )
    return t

class _JudgeQueue:

    def get_task_queue( self ):
        return self.manager.get_task_queue()
    
    def get_result_queue( self ):
        return self.manager.get_result_queue()

    def init_push_waiting_submission(self):
        try:
            f = Submission.objects.filter( judge_status = 'Waiting' )
            for _ in f:
                self.push_submission( _ )
        except Exception as e:
            print( '- Init push waiting submission failed:' , str( e ) )
        print( '- Init push waiting submission completed,' , str( len( f ) ) + '(s) waiting submissions.' )

    def push_submission( self , submission ):
        print( 'push' )
        ret = self.task.put( submission.get_push_dict() )
        print( 'push completed' , ret , self.task.qsize() )

    def Modify_submission_status( self , ** report ):
        submission = report[ 'submission' ]
        case = report[ 'case' ]
        result = report[ 'result' ]
        complete = report[ 'complete' ]
        if result == 'Running':
            Submission.objects.filter( submission_id = submission ).update( judge_status = 'Running on test ' + str( case ) )
        else:
            sub = Submission.objects.get( submission_id = submission )
            Judgeinfo(
                submission = sub,
                ** get_update_dict( report )).save()
            if complete == True:
                Submission.objects.filter( submission_id = submission ).update( judge_status = result , completed = True )


    def read_modify_status( self ):
        while True:
            s = self.result.get( block = True )
            self.Modify_submission_status( ** s )

    def __init__( self ):
        QueueManager.register('get_task_queue', callable=lambda: task_queue)
        QueueManager.register('get_result_queue', callable=lambda: result_queue)
        self.manager = QueueManager( address=('0.0.0.0', JUDGE_PORT), authkey = JUDGE_AUTH_KEY )        
        self.manager.connect()
        self.task = self.get_task_queue()
        self.result = self.get_result_queue()
        self.init_push_waiting_submission()
        Thread( target = self.read_modify_status , daemon = True ).start()

modules[__name__] = _JudgeQueue()