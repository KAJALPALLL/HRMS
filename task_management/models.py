from django.db import models
from user_management.models import Employee

class TaskManagement(models.Model):
    status = models.CharField(default='open',null=True, max_length=100)
    priority = models.CharField(default='high',null=True, max_length=100)
    image = models.FileField(upload_to='task-management/',default=None,null=True)
    datetime = models.DateTimeField(auto_now_add=True)
    description = models.CharField(default=None,null=True, max_length=100)
    task_assign_to = models.ManyToManyField(Employee,related_name='lily')
    task_assign_from = models.ManyToManyField(Employee,related_name='john')

    class Meta:
        db_table = 'task_management'



class TaskConversation(models.Model):
    mimetype = models.TextField(default=None, null=True)
    text = models.TextField(default=None, null=True)
    image = models.FileField(upload_to='task-convo', default=None, null=True)
    task = models.ForeignKey(TaskManagement, on_delete=models.SET_DEFAULT, default=None, null=True)
    datetime = models.DateTimeField(auto_now_add=True)
    message_by = models.ForeignKey(Employee,on_delete=models.CASCADE,default=None,null=True)

    class Meta:
        db_table = 'task_conversation'


