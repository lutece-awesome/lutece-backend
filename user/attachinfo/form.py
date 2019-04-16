from django import forms

from user.attachinfo.constant import MAX_ABOUT_LENGTH, MAX_COMPANY_LENGTH, MAX_LOCATION_LENGTH, MAX_SCHOOL_LENGTH, \
    MAX_CODEFORCESNAME_LENGTH, MAX_ATCODERNAME_LENGTH, MAX_STUDENTID_LENGTH


class AttachInfoForm(forms.Form):
    about = forms.CharField(required=False, max_length=MAX_ABOUT_LENGTH)
    school = forms.CharField(required=False, max_length=MAX_SCHOOL_LENGTH)
    company = forms.CharField(required=False, max_length=MAX_COMPANY_LENGTH)
    location = forms.CharField(required=False, max_length=MAX_LOCATION_LENGTH)
    # gravatar = forms.CharField( required = False , max_length = MAX_GRAVATAR_LENGTH )
    codeforces = forms.CharField(required=False, max_length=MAX_CODEFORCESNAME_LENGTH)
    atcoder = forms.CharField(required=False, max_length=MAX_ATCODERNAME_LENGTH)
    studentid = forms.CharField(required=False, max_length=MAX_STUDENTID_LENGTH)
    gender = forms.BooleanField(required=False)