from annoying.functions import get_object_or_None
from django import forms

from reply.models import AbstractReply


class AbstractReplyForm(forms.Form):
    content = forms.CharField(required=True, max_length=1024)
    parent = forms.IntegerField(required=True)

    def clean(self):
        cleaned_data = super().clean()
        parent = cleaned_data.get('parent')
        par = get_object_or_None(AbstractReply, pk=parent)
        if par is None:
            self.add_error('parent', 'Unknown reply parent node')
