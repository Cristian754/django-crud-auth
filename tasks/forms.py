from django.forms import ModelForm
from .models import Task
from django import forms

class TaskForm(forms.ModelForm):
  class Meta:
    model = Task
    fields = ['title', 'description', 'important']
    widgets = {
      'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Add new task...'}),
      'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Add description...'}),
      'important': forms.CheckboxInput(attrs={'class': 'form-chech-input'}),
    }