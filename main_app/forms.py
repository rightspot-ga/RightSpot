from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(label='Email Address')
    first_name = forms.CharField(max_length=100, label='First Name', required=False)
    last_name = forms.CharField(max_length=100, label='Last Name', required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name') + UserCreationForm.Meta.fields + ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'email' in self.data:
            self.fields['email'].initial = self.data['email']

class EditUserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, label='First Name', required=False)
    last_name = forms.CharField(max_length=100, label='Last Name', required=False)
    email = forms.EmailField(label='Email Address')

    class Meta:
        model = User
        fields =  ('first_name', 'last_name','username', 'email',)
