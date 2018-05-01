from .models import Submission

def get_update_dict( dic ):
    for _ in dic:
        if _ not in Submission.Judge.update_field:
            dic.pop( _ )
    return dic