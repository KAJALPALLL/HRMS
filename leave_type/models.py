from django.db import models
from user_management.models import Employee

# class Leave(models.Model):
#     name = models.TextField(default=None,null=True)
#     value = models.TextField(default=None,null=True)
#     status = models.TextField(default='Active',null=True)
#     datetime = models.DateField(auto_now_add=True)

# Request or Assign or Apply ????


# class LeaveRequest(models.Model):
#     leave_type = models.ForeignKey(Leave,on_delete=models.CASCADE,default=None,null=True)
#     employee = models.ForeignKey(Employee,on_delete=models.CASCADE,default=None,null=True)
#     start_date = models.DateField(default=None,null=True)
#     end_date = models.DateField(default=None,null=True)
#     leave_reason = models.TextField(default=None,null=True)
#     datetime = models.DateField(auto_now_add=True)
#     status = models.TextField(default=None,null=True)
    # approved_by = models.ForeignKey(employee,on_delete=models.CASCADE,default=None,null=True)
