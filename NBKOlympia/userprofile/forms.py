from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import MyUser
from django.utils import timezone

# Custom creation form for MyUser
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = MyUser
        fields = ("username", "first_name", "last_name", "display_name", "profile_pic", "is_contestant")
