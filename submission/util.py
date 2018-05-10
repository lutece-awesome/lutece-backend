from .models import Submission
from Lutece.config import SUPPORT_LANGUAGE_LIST

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
    return SUPPORT_LANGUAGE_LIST[lang]