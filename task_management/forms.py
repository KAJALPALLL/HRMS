from django import forms
from . models import TaskManagement
from user_management.models import Employee


priority = (('1','High'),('2','Medium'),('3','Low'))

employee = Employee.objects.filter(groups__name='employee')

class TaskForm(forms.ModelForm):
    description = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Query, please provide the exact details of your issue in a descriptive manner which help us to understand your query.'}))
    priority = forms.CharField(widget=forms.Select(choices=priority,attrs={'class':'form-control'}))
    image = forms.FileField(label='Select Image')

    class Meta:
        model = TaskManagement
        fields = ('description','priority','image')