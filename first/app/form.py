from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Customer

class signUp(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email']


class ProfileForm(forms.ModelForm):
    class Meta:
        model=Customer
        fields='__all__'

