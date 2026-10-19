from django import forms
from . models import Tickets
from user_management.models import Department


priority = (('1','High'),('2','Medium'),('3','Low'))

department = Department.objects.all()

class TicketForm(forms.ModelForm):
    description = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Query, please provide the exact details of your issue in a descriptive manner which help us to understand your query.'}))
    priority = forms.CharField(widget=forms.Select(choices=priority,attrs={'class':'form-control'}))
    image = forms.FileField(label='Select Image')
    department = forms.ModelChoiceField(queryset=department)

    class Meta:
        model = Tickets
        fields = ('description','priority','image','department')