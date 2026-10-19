from django.urls import path
from . import views

urlpatterns = [
    path('add-task',views.add_task,name='add_task'),
    path('task-list', views.task_list, name='task_list'),
    path('update-task/<str:id>',views.update_task,name='update_task'),
    path('delete-task/<str:id>', views.delete_task, name='delete_task'),
    path('task-conversation/<str:id>',views.task_conversation,name='task_conversation'),
    path('delete-task-conversation/<str:id>',views.delete_task_conversation,name='delete_task_conversation'),


    path('employee-task-list',views.employee_task_list,name='employee_task_list'),
    path('task-status-update/<str:id>',views.task_status_update,name='task_status_update'),
    path('add-task-conversation',views.add_task_conversation,name='add_task_conversation'),
    path('open-task-list',views.open_task_list,name='open_task_list'),
    path('closed-task-list', views.closed_task_list, name='closed_task_list'),

]