from annoying.functions import get_object_or_None
from django import forms

from reply.models import BaseReply


class BaseReplyForm(forms.Form):
    content = forms.CharField(required=True, max_length=1024)
    parent = forms.IntegerField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        parent = cleaned_data.get('parent')
        # If this reply have parent, check it
        if parent:
            par = get_object_or_None(BaseReply, pk=parent)
            if par is None:
                self.add_error('parent', 'Unknown reply parent node')
