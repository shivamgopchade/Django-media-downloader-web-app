from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import media

class UserRegisterForm(UserCreationForm):
    age=forms.IntegerField(min_value=18)
    email=forms.EmailField()

    class Meta:
        model=User
        fields=['username','email','age','password1','password2']

class UserMediaForm(forms.ModelForm):
    class Meta:
        model=media
        fields=['file']