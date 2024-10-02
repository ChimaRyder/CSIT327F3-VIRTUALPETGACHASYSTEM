from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class SignupForm(UserCreationForm):
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
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        #user.set_password(self.cleaned_data['password'])
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user
    
class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={
        'class': 'auth-input'
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'auth-input'
    }))