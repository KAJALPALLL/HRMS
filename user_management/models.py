from django.db import models

from django.contrib.auth.models import AbstractUser

class Department(models.Model):
    name = models.TextField(default=None,null=True)
    status = models.TextField(default=None,null=True)
    datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'department'

    def __str__(self):
        return self.name




class Employee(AbstractUser):
    name = models.TextField(default=None, null=True)
    father_name = models.TextField(default=None, null=True)
    date_of_birth = models.DateField(default=None, null=True)
    gender = models.TextField(default=None, null=True)
    department = models.ForeignKey(Department,on_delete=models.CASCADE,default=None,null=True)

    # documents
    aadhar_number = models.TextField(default=None, null=True, unique=True)
    pan_number = models.TextField(default=None, null=True, unique=True)
    passport_number = models.TextField(default=None, null=True, unique=True)
    calling_number = models.TextField(default=None, null=True, unique=True)
    whatsapp_number = models.TextField(default=None,null=True)

    # address
    address = models.TextField(default=None, null=True)
    state = models.TextField(default=None, null=True)
    city = models.TextField(default=None, null=True)
    postal_code = models.TextField(default=None, null=True)
    profile_image = models.ImageField(upload_to='employee/', default=None, null=True)

    class Meta:
        db_table = 'auth_user'

    # def __str__(self):
    #     return self.username
    #


class EmployeeDocument(models.Model):
    name = models.TextField(default=None,null=True)
    image = models.ImageField(upload_to='document/',default=None,null=True)
    datetime = models.DateTimeField(auto_now_add=True)
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE,default=None,null=True)

    class Meta:
        db_table = 'documents'



