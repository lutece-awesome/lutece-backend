import graphene
from submission.models import Submission
from submission.type import SubmissionType

class Query(object):
    submission = graphene.Field( SubmissionType , pk = graphene.ID() )

    def resolve_submission( self , info , pk ):
        return Submission.objects.get( pk = self.pk )