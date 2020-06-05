from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import ModelForm


class UserRegisterForm(UserCreationForm):

	email = forms.EmailField()

	class Meta:
		model = User
		fields = [ 'username', 'email', 'password1', 'password2']

class UpdateForm(ModelForm):
	email = forms.EmailField()
	class Meta:
		model = User
		fields = ['username','email']

class ProfileUpdateForm(ModelForm):
	class Meta:
		model = User
		fields = []