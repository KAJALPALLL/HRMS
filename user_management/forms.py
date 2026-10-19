from . models import Employee, EmployeeDocument, Department
from django import forms


gender = [('Male','Male'),('Female','Female'),('Other','Other')]


class EmployeeForm(forms.ModelForm):
    # name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Name'}))
    father_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Father Name'}))
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control','type':'date'}))
    gender = forms.CharField(widget=forms.Select(choices=gender, attrs={'class': 'form-control'}))
    department = forms.ModelChoiceField(queryset=Department.objects.all())
    # documents
    aadhar_number = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Aadhar Number'}))
    pan_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Pan Number'}),required=False)
    passport_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Passport Number'}),required=False)
    whatsapp_number = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Whatsapp Number'}))
    calling_number = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Calling Number'}))
    # address
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Address'}))
    state = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter State'}))
    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter City'}))
    postal_code = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control','placeholder':'Enter Postal Code'}))
    profile_image = forms.ImageField(label='Select Image')

    class Meta:
        model = Employee
        fields = ( 'profile_image', 'postal_code', 'city', 'state', 'address',
                  'calling_number', 'passport_number','pan_number',
                  'aadhar_number', 'father_name', 'date_of_birth', 'gender','whatsapp_number','department')



class EmployeeDocumentForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Document Name'}))
    image = forms.ImageField(label='Select Image')

    class Meta:
        model = EmployeeDocument
        fields = ('name','image')



