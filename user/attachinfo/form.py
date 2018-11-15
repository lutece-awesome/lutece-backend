from django import forms

from user.attachinfo.constant import MAX_ABOUT_LENGTH, MAX_COMPANY_LENGTH, MAX_LOCATION_LENGTH, MAX_SCHOOL_LENGTH


class AttachInfoForm(forms.Form):
    about = forms.CharField(required=False, max_length=MAX_ABOUT_LENGTH)
    school = forms.CharField(required=False, max_length=MAX_SCHOOL_LENGTH)
    company = forms.CharField(required=False, max_length=MAX_COMPANY_LENGTH)
    location = forms.CharField(required=False, max_length=MAX_LOCATION_LENGTH)
    # gravatar = forms.CharField( required = False , max_length = MAX_GRAVATAR_LENGTH )
