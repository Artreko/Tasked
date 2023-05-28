from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Imports for Reordering Feature
from django.views import View
from django.shortcuts import redirect
from django.db import transaction

from datetime import date
from operator import attrgetter
import logging

from .models import Task
from .forms import SignupForm, TaskForm, CreateTaskForm, UpdateTaskForm

logger = logging.getLogger(__name__)


class CustomLoginView(LoginView):
    template_name = 'taskedapp/login.html'
    fields = '__all__'
    required_css_class = "field"
    redirect_authenticated_user = True

    # def get_success_url(self):
    #     return reverse_lazy('tasks')


class RegisterPage(FormView):
    template_name = 'taskedapp/register.html'
    form_class = SignupForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        uncompleted_tasks = context['tasks'].filter(complete=False)
        completed_tasks = context['tasks'].filter(complete=True)
        uncompleted_tasks = context['tasks'].filter(complete=False)
        context['count'] = uncompleted_tasks.count()
        uncompleted_tasks = list(uncompleted_tasks)
        # logger.debug(f'{uncompleted_tasks}')
        tasks_no_deadline = []
        idx = 0
        while idx < len(uncompleted_tasks):
            task = uncompleted_tasks[idx]
            # logger.debug(f'{task} {task.deadline}')
            if not task.deadline:
                tasks_no_deadline.append(task)
                uncompleted_tasks.pop(idx)
                idx -= 1
            idx += 1
        logger.debug(f'{uncompleted_tasks}, {tasks_no_deadline}')
        uncompleted_tasks = sorted(uncompleted_tasks, key=attrgetter('deadline'))
        context['danger'] = [task for task in uncompleted_tasks 
                                if task.deadline and task.deadline <= date.today()]
        context['tasks'] = [*uncompleted_tasks, *tasks_no_deadline, *completed_tasks]
        return context


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    form_class = CreateTaskForm
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskEdit(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = UpdateTaskForm
    # fields = ['title', 'description', 'complete', 'deadline']
    success_url = reverse_lazy('tasks')

    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(user=owner)


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')

    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(user=owner)
