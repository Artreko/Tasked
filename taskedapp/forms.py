from django import forms
from django.contrib.auth.forms import UserCreationForm  
from django.contrib.auth.models import User  
# Reordering Form and View


class PositionForm(forms.Form):
    position = forms.CharField()

class SignupForm(UserCreationForm):  
    email = forms.EmailField(max_length=200, help_text='Required')  
    class Meta:  
        model = User  
        fields = ('username', 'email', 'password1', 'password2')  
