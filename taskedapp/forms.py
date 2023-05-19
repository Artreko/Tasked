from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Task
from datetime import date

# Reordering Form and View


class SignupForm(UserCreationForm):  
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:  
        model = User  
        fields = ('username', 'email', 'password1', 'password2')
        labels = {
            'username': 'Логин'
        }


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'complete', 'deadline', 'description', ]
        localized_fields = '__all__'
        widgets = {
            'title': forms.TextInput(
                attrs={
                'class': 'task-title',
                'type': 'text',
                'placeholder': 'Название',
                }
            ),
            'deadline': forms.DateInput(format='%Y-%m-%d', attrs={
                'class': 'date-class',
                'type': 'date',
            }),
            'description': forms.Textarea(attrs={
                'class': 'task-description',
                'placeholder': 'Описание',
                })
        }
        labels = {
            'title': 'Название',
            'completed': 'Завершено',
            'description': 'Описание',
            'deadline': 'Крайний срок',
        }