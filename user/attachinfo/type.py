from graphene_django.types import DjangoObjectType
from user.attachinfo.models import AttachInfo

class AttachInfoTypeMixin( DjangoObjectType ):
    class Meta:
        model = AttachInfo
        only_fields = ( 'school' , 'company' , 'location' , 'about' )