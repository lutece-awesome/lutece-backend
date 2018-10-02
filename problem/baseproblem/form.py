from django import forms
from problem.baseproblem.constant import MAX_TITLE_LENGTH, MAX_CONTENT_LENGTH, MAX_RESOURCES_LENGTH, MAX_CONSTRAINTS_LENGTH, MAX_NOTE_LENGTH

class AbstractProblemForm( forms.Form ):
    title = forms.CharField( required = True , max_length = MAX_TITLE_LENGTH )
    content = forms.CharField( required = True , max_length = MAX_CONTENT_LENGTH )
    resources = forms.CharField( required  = True , max_length = MAX_RESOURCES_LENGTH )
    constraints = forms.CharField( required = True , max_length = MAX_CONSTRAINTS_LENGTH )
    note = forms.CharField( required = True , max_length = MAX_NOTE_LENGTH )