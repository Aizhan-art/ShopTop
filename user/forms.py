from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import MyUser

class UserRegisterForms(UserCreationForm):

    class Meta:
        model = MyUser
        fields = ('first_name', 'email', 'phone_number')


class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = MyUser
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'avatar']
