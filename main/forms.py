from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import re

class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=500, required=True)

    class Meta:
        model = User
        fields = ['username' , 'email' , 'password1' , 'password2']

    #password requirements
    def clean_password1(self):
        password = self.cleaned_data.get('password1')

        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters length")

        if not re.search(r'\d', password):
            raise forms.ValidationError("Password must contain at least 1 number")

        if not re.search(r'[A-Z]', password):
            raise forms.ValidationError("Password must contain at least 1 uppercase letter")

        return password

    #password match
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")

        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'placeholder': 'Enter your username'}))
    password = forms.CharField(max_length=128, widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}))
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')


class EditProfileForm(forms.ModelForm):
    username = forms.CharField(max_length= 100, required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Enter your username'}))

    email = forms.EmailField(max_length=500, required=True,
                              widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'}))

    name = forms.CharField(max_length=150, required=False,
                           widget=forms.TextInput(attrs={'placeholder': 'Enter your name(Optional)'}))

    phone_number = forms.CharField(max_length=15, required=False,
                                   widget=forms.TextInput(attrs={'placeholder': 'Enter your phone number(Optional)'}))

    age = forms.IntegerField(required=False, min_value=0 ,
                             widget=forms.TextInput(attrs={'placeholder': 'Enter your age(Optional)'}))

    bio = forms.CharField(max_length=1000, required=False,
                          widget=forms.Textarea(attrs={'placeholder': 'Enter your bio (Optional)', 'rows': 4}))

    class Meta:
        model = User
        fields = ['username', 'email', 'name', 'phone_number', 'age', 'bio']