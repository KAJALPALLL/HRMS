from django.db import models
from user_management.models import Employee



class LeaveType(models.Model):
    name = models.TextField(default=None,null=True)
    value = models.TextField(default=None,null=True)
    status = models.TextField(default='Active',null=True)
    datetime = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'leave'

    def __str__(self):
        return self.name



class LeaveRequest(models.Model):
    day_type = models.CharField(default=None,null=True, max_length=100)
    leave_type = models.ForeignKey(LeaveType,on_delete=models.CASCADE,default=None,null=True)
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE,default=None,null=True)
    start_date = models.DateField(default=None,null=True)
    end_date = models.DateField(default=None,null=True)
    leave_reason = models.TextField(default=None,null=True)
    datetime = models.DateTimeField(auto_now_add=True)
    status = models.TextField(default='pending',null=True)
    days = models.TextField(default=None,null=True)
    approved_date = models.DateField(default=None,null=True)
    approved_by = models.ForeignKey(Employee,on_delete=models.CASCADE,default=None,null=True,related_name='approver')

    class Meta:
        db_table = 'leave_request'

    def __str__(self):
        return self.employee.username



# per employee leaves define

class EmployeeLeave(models.Model):
    leave_type = models.ForeignKey(LeaveType,on_delete=models.CASCADE,default=None,null=True)
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE,default=None,null=True)
    values = models.TextField(default=None,null=True)
    status = models.TextField(default=None,null=True)

    class Meta:
        db_table = 'per_employee_leave'



class LeaveHistory(models.Model):
    # employee = models.ForeignKey(Employee,on_delete=models.CASCADE,default=None,null=True)
    employee_leave_type = models.ForeignKey(EmployeeLeave,on_delete=models.CASCADE,default=None,null=True)
    description = models.TextField(default=None,null=True)
    added_by = models.ForeignKey(Employee,on_delete=models.CASCADE,default=None,null=True)
    status = models.TextField(default=None,null=True)
    value = models.TextField(default=None,null=True)
    datetime = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'leave_history'
