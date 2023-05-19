from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Task
from datetime import date
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
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

class CreateTaskForm(TaskForm):
    def clean_deadline(self):
        data = self.cleaned_data["deadline"]
        if data and data < date.today():
            raise ValidationError(_("Неправильная дата - крайний срок не может быть в прошлом"))
        return data

class UpdateTaskForm(TaskForm):
    def clean_deadline(self):
        data = self.cleaned_data["deadline"]
        if data:
            current_date = self.instance.deadline
            if current_date:
                current_date = currend_date.date()
                today = date.today()
                if current_date < today and data< current_date:
                    raise ValidationError(_("Неправильная дата - крайний срок не может быть раньше текущего"))
                elif data < today:
                    raise ValidationError(_("Неправильная дата - крайний срок не может быть в прошлом"))
        return data   