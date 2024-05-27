from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.shortcuts import render
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required

def index(request):
  return render(request, 'main/index.html')

def sign_up(request):
  if request.method == 'GET':
    return render(request, 'login-register/signup.html', { 'form': UserCreationForm() })
  else:
    if request.POST['password1'] == request.POST['password2']:
      try:
        user = User.objects.create_user(
        username=request.POST['username'],
        password=request.POST['password1']
        )
        user.save()
        login(request, user)
        return redirect('index')
      except IntegrityError:
        return render(request, 'login-register/signup.html', {
          'form': UserCreationForm(),
          'error': 'Username already exists'
          })
    return render(request, 'login-register/signup.html', {
      'form': UserCreationForm(),
      'error': 'Passwords do not match'
      })

@login_required
def tasks(request):
  tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
  return render(request, 'tasks/tasks.html', { 'tasks': tasks })

@login_required
def signout(request):
  logout(request)
  return redirect('index')

def signin(request):
  if request.method == 'GET':
    return render(request, 'login-register/signin.html', { 'form': AuthenticationForm() })
  else:
    user = authenticate(
      request,
      username=request.POST['username'],
      password=request.POST['password']
      )
    if user is None:
      return render(request, 'login-register/signin.html', {
        'form': AuthenticationForm(),
        'error': 'Username or password dot match'
        })
    else:
      login(request, user)
      return redirect('index')

@login_required
def create_task(request):
  if request.method == 'GET':
    return render(request, 'tasks/create_task.html', { 'form': TaskForm() })
  else:
    try:
      form = TaskForm(request.POST)
      new_task = form.save(commit=False)
      new_task.user = request.user
      new_task.save()
      return redirect('tasks')
    except ValueError:
      return render(request, 'tasks/create_task.html', {
        'form': TaskForm(),
        'error': 'Please provide valid data.'
        })

@login_required
def task_detail(request, task_id):
  if request.method == 'GET':
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    form = TaskForm(instance=task)
    return render(request, 'tasks/task_detail.html', { 'task': task, 'form': form })
  else:
    try:
      task = get_object_or_404(Task, pk=task_id, user=request.user)
      form = TaskForm(request.POST, instance=task)
      form.save()
      return redirect('tasks')
    except ValueError:
      return render(request, 'tasks/task_detail.html', {
        'task': task,
        'form': form,
        'error': 'Error updating task.'
        })

@login_required
def task_complete(request, task_id):
  task = get_object_or_404(Task, pk=task_id, user=request.user)
  if request.method == 'POST':
    task.datecompleted = timezone.now()
    task.save()
    return redirect('tasks')

@login_required
def task_delete(request, task_id):
  task = get_object_or_404(Task, pk=task_id, user=request.user)
  if request.method == 'POST':
    task.delete()
    return redirect('tasks')

@login_required
def task_completed(request):
  tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
  return render(request, 'tasks/tasks.html', { 'tasks': tasks })
