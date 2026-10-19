from . models import LeaveType,LeaveRequest,LeaveHistory

from django import forms

status = [('Active','Active'),('InActive','InActive')]

class LeaveTypeForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Name'}))
    value = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'Enter Value','max':10}))
    status = forms.CharField(widget=forms.Select(choices=status,attrs={'class':'form-control'}),required=False)

    class Meta:
        model = LeaveType
        fields = ('name','value','status')


leave_status = [('Accepted','Accepted'),('Denied','Denied'),('Pending','Pending')]


class UpadteLeaveRequestForm(forms.ModelForm):
    leave_type = forms.ModelChoiceField(queryset=LeaveType.objects.all())
    start_date = forms.DateField(widget=forms.DateInput(attrs={'class':'form-control','type':'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'class':'form-control','type':'date'}))
    leave_reason = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Reason'}))

    class Meta:
        model = LeaveRequest
        fields = ('start_date','end_date','leave_reason','leave_type')



class LeaveHistoryForm(forms.ModelForm):
    value = forms.FloatField(widget=forms.NumberInput(attrs={'class':'form-control'}))
    description = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Reason'}))

    class Meta:
        model = LeaveHistory
        fields = ('value','description')