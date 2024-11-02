from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Profile
import random

AVATAR_CHOICES = [
    'avatar1.png',
    'avatar2.png',
    'avatar3.png',
    'avatar4.png',
]

class SignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={
        'class': 'auth-input',
        'autofocus': 'autofocus',
    }))
    
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={
        'class': 'auth-input'
    }))

    birthdate = forms.DateField(required=True, widget=forms.DateInput(attrs={
        'class': 'auth-input',
        'type': 'date'
    }))
    
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'auth-input'
    }))

    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'auth-input'
    }))

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={
        'class': 'auth-input'
    }))

    password2 = forms.CharField(label="Retype Password", widget=forms.PasswordInput(attrs={
        'class': 'auth-input'
    }))


    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'birthdate', 'username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        #user.set_password(self.cleaned_data['password'])
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
            profile, created = Profile.objects.get_or_create(user=user)
            profile.first_name = self.cleaned_data['first_name']
            profile.last_name = self.cleaned_data['last_name']
            profile.birthdate = self.cleaned_data['birthdate']
            profile.total_credits = 500
            profile.avatar = random.choice(AVATAR_CHOICES)
            profile.save()

        return user
    
class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={
        'class': 'auth-input'
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'auth-input'
    }))