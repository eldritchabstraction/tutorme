from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from . models import Profile

class SignupForm(UserCreationForm):
	model = User
	first_name = forms.CharField(max_length=30)
	last_name = forms.CharField(max_length=30)
	birth_date = forms.DateField(help_text="Required. Format: YYYY-MM-DD")
	email = forms.EmailField(max_length=120,help_text="Required. Please input a valid e-mail address")
	fields = ("username", "password1", "password2", "first_name", "last_name", "birth_date", "email")
