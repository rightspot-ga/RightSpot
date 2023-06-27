from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from .models import Project, Location


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
        self.fields['username'].help_text = 'Max 150 characters. Only letters, digits and @/./+/-/_ allowed.'
        self.fields['password1'].help_text = mark_safe("<ul><li>Cannot be too similar to your other personal information.</li><li>Must be at least 8 characters.</li><li>Cannot be a commonly used password.</li><li>Cannot be entirely numeric.</li></ul>")
        self.fields['password2'].help_text = 'Please re-type your password'
        self.fields['password1'].label = 'Password <span class="text-danger ms-1">*<span>'
        self.fields['password2'].label = 'Confirm Password <span class="text-danger ms-1">*<span>'
        self.fields['first_name'].label = 'First Name <small class="text-white ms-2 fw-light">optional<small>'
        self.fields['last_name'].label = 'Last Name <small class="text-white ms-2 fw-light">optional<small>'
        self.fields['email'].label = 'Email Address <span class="text-danger ms-1">*<span>'
        self.fields['username'].label = 'Username <span class="text-danger ms-1">*<span>'


class EditUserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, label='First Name', required=False)
    last_name = forms.CharField(max_length=100, label='Last Name', required=False)
    email = forms.EmailField(label='Email Address')

    class Meta:
        model = User
        fields =  ('first_name', 'last_name','username', 'email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prefix = 'edit_user'
        self.fields['username'].help_text = 'Max 150 characters. Only letters, digits and @/./+/-/_ allowed.'

class CustomPasswordChangeForm(PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].label = 'Current Password'
        self.fields['new_password1'].label = 'New Password'
        self.fields['new_password2'].label = 'Confirm New Password'
        self.fields['new_password1'].help_text = mark_safe("<ul><li>Cannot be too similar to your other personal information.</li><li>Must be at least 8 characters.</li><li>Cannot be a commonly used password.</li><li>Cannot be entirely numeric.</li></ul>")
        self.prefix = 'password_change'

class ProjectUpdateForm(forms.ModelForm):
    locations = forms.ModelMultipleChoiceField(queryset=Location.objects.none(), widget=forms.CheckboxSelectMultiple(), required=False)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ProjectUpdateForm, self).__init__(*args, **kwargs)

        if user:
            self.fields['locations'].queryset = Location.objects.filter(user=user)
        if self.instance and self.instance.pk:
            self.fields['locations'].initial = self.instance.location_set.all()

    class Meta:
        model = Project
        fields = ['name', 'description', 'locations']

class LocationUpdateForm(forms.ModelForm):
    projects = forms.ModelMultipleChoiceField(queryset=Project.objects.none(), widget=forms.CheckboxSelectMultiple())

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(LocationUpdateForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['projects'].required = False
            self.fields['projects'].queryset = Project.objects.filter(location__user=user).distinct()
            if self.instance:
                self.fields['projects'].initial = self.instance.projects.all()

    class Meta:
        model = Location
        fields = ['name', 'description', 'projects']        

