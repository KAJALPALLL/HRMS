from . models import Leave,LeaveRequest

from django import forms

status = [('Active','Active'),('InActive','InActive')]

class LeaveForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Name'}))
    value = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'Enter Value'}))
    status = forms.CharField(widget=forms.Select(choices=status,attrs={'class':'form-control'}),required=False)

    class Meta:
        model = Leave
        fields = ('name','value','status')


leave_status = [('Accepted','Accepted'),('Denied','Denied'),('Pending','Pending')]


class LeaveRequestForm(forms.ModelForm):
    leave_type = forms.ModelChoiceField(queryset=Leave.objects.all())
    start_date = forms.DateField(widget=forms.DateInput(attrs={'class':'form-control','type':'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'class':'form-control','type':'date'}))
    status = forms.CharField(widget=forms.Select(choices=leave_status,attrs={'class':'form-control'}))
    leave_reason = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = LeaveRequest
        fields = ('leave_type','start_date','end_date','status','leave_reason')
