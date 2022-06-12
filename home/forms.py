from django import forms
from user.models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserForm(UserCreationForm):
    class Meta:
        model = Profile
        fields = (
            "username",
            "instagram_password",
        )
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "style": "max-width: 300px;",
                    "placeholder": "Username",
                }
            ),
            "instagram_password": forms.PasswordInput(
                attrs={
                    "class": "form-control",
                    "style": "max-width: 300px;",
                    "placeholder": "Instagram Password",
                }
            ),
        }
