from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('signup/', views.sign_up, name='sign_up'),
  path('tasks/', views.tasks, name='tasks'),
  path('logout/', views.signout, name='logout'),
  path('signin/', views.signin, name='sign_in'),
  path('create_task/', views.create_task, name='create_task'),
  path('task_detail/<int:task_id>', views.task_detail, name='task_detail'),
  path('task_complete/<int:task_id>', views.task_complete, name='task_complete'),
  path('task_completed/', views.task_completed, name='task_completed'),
  path('task_delete/<int:task_id>', views.task_delete, name='task_delete'),
]
