from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email"]


class LoginForm(forms.Form):
    username = forms.CharField(label="Username or Email")
    password = forms.CharField(widget=forms.PasswordInput)
