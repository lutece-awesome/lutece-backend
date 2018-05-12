from .models import Submission, Judgeinfo
from Lutece.config import PRISM_LANGUAGE

def get_update_dict( dic ):
    L = []
    t = dic
    for _ in t:
        if _ not in Submission.Judge.update_field:
            L.append( _ )
    for _ in L:
        t.pop( _ )
    return t


def prism_name_transfer( lang ):
    return PRISM_LANGUAGE[lang]
