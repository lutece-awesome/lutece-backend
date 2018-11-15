from django import forms

from problem.limitation.constant import MAX_TIME_LIMITATION, MIN_TIME_LIMITATION, MAX_MEMORY_LIMITATION, \
    MIN_MEMORY_LIMITATION, MAX_OUTPUT_LIMITATION, MIN_OUTPUT_LIMITATION, MAX_CPU_LIMITATION, MIN_CPU_LIMITATION


class LimitationForm(forms.Form):
    time_limit = forms.IntegerField(required=True, max_value=MAX_TIME_LIMITATION, min_value=MIN_TIME_LIMITATION)
    memory_limit = forms.IntegerField(required=True, max_value=MAX_MEMORY_LIMITATION, min_value=MIN_MEMORY_LIMITATION)
    output_limit = forms.IntegerField(required=False, max_value=MAX_OUTPUT_LIMITATION, min_value=MIN_OUTPUT_LIMITATION)
    cpu_limit = forms.IntegerField(required=False, max_value=MAX_CPU_LIMITATION, min_value=MIN_CPU_LIMITATION)
