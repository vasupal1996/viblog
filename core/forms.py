from django import forms
from django.contrib.auth.models import User

from authentication.models import UserProfile

class UserForm(forms.ModelForm):

    # dob = forms.DateField(input_formats=['%d-%m-%Y'])
    # state = forms.CharField()
    # country = forms.CharField()
    # mobile = forms.IntegerField()
    # alternate_email = forms.EmailField()
    # intro_slogan = forms.CharField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name' ]

class UserProfileForm(forms.ModelForm):
    dob = forms.CharField(widget=forms.TextInput(attrs={'type':'date'}))
    class Meta:
        model = UserProfile
        fields = ['dob','state', 'country', 'mobile', 'alternate_email', 'intro_slogan']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['dob'].widget.format = '%d-%m-%Y'
        self.fields['dob'].input_formats = ['%d-%m-%Y']

class UserImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_image']

    