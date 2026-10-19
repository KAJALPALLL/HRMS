from django.db import models

from user_management.models import Department,Employee

class Tickets(models.Model):
    department = models.ForeignKey(Department,on_delete=models.SET_DEFAULT,default=None,null=True)
    client = models.ForeignKey(Employee,on_delete=models.SET_DEFAULT,default=None,null=True)
    status = models.TextField(default='open',null=True)
    priority = models.IntegerField(default=None,null=True)
    image = models.FileField(upload_to='ticket-query',default=None,null=True)
    description = models.TextField(default=None,null=True)
    datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tickets'


class TicketConversation(models.Model):
    employee = models.ForeignKey(Employee,on_delete=models.SET_DEFAULT,default=None,null=True,related_name='employee_reply')
    client = models.ForeignKey(Employee,on_delete=models.SET_DEFAULT,default=None,null=True,related_name='client_reply')
    mimetype = models.TextField(default=None,null=True)
    text = models.TextField(default=None,null=True)
    image = models.FileField(upload_to='ticket-convo',default=None,null=True)
    ticket = models.ForeignKey(Tickets,on_delete=models.SET_DEFAULT,default=None,null=True)
    datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ticket_conversation'






