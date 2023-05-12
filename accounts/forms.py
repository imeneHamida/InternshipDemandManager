from django import forms
from django.forms import ModelForm 
from .models import *
from django.forms import ModelForm, TextInput, EmailInput

class CreationUserForm(forms.Form):
    username = forms.CharField(
        max_length=9,
        widget=forms.TextInput(attrs={"placeholder": "Enter Your Matric Number"}),
    )

    email = forms.EmailField(
        max_length=255,
        widget=forms.EmailInput(attrs={"placeholder": "Enter Your E-mail Address"}),
    )

    password = forms.CharField(
        max_length=255,
        widget=forms.PasswordInput(
            attrs={"placeholder": "Enter Your Password", "id": "password"}
        ),
    )

    password2 = forms.CharField(
        max_length=255,
        widget=forms.PasswordInput(
            attrs={"placeholder": "Confirm Your Password", "id": "password2"}
        ),
    )
 
class CreationIntenApp(ModelForm):
    class Meta:
        model = InternshipApp
        fields = '__all__'
        widgets = {
        'applicant': forms.Select(attrs={'class': 'form-control'}),
        'studentdep': forms.TextInput(attrs={'class': "form-control",'style': 'max-width: 100%; overflow: auto;','placeholder': 'Department..'}),
        'studentCard': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Your Card Number..'}),
        'studentSnum': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Social Security Number..'}),
        'studenTel': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Your Phone Number..'}),
        'prepDeplome': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Licsense/Master..'}),
        'sprvisorName': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Supervisor full name..'}),
        'sprvisorEmail': forms.EmailInput(attrs={'class': 'form-control','placeholder':"example@univ-constantine2.dz"}),
        'sprvisorTel': forms.TextInput(attrs={'class': 'form-control','placeholder': '### ### ### ###'}),
        'sprvisorFax': forms.TextInput(attrs={'class': 'form-control','placeholder': '### ### ### ###'}),
        'companyName': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Department..'}),
        'companyAdrss': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Street Address..'}),
        'theme': forms.Textarea(attrs={'class': 'form-control','placeholder': 'Explain Theme of the intenrship..','rows':3, 'cols':5,'style': 'max-width: 100%; Height: 100px;overflow: auto;'}),
        'duree' : forms.TextInput(attrs={'class': 'form-control','placeholder': 'Period..'}),
        'strtDate': forms.DateInput(attrs={'class': 'form-control','placeholder': 'Year-Month-Day.'}),
        'endDate': forms.DateInput(attrs={'class': 'form-control','placeholder': 'Year-Month-Day.'}),}  


class CreationIntenApp(ModelForm):
    class Meta:
        model = InternshipApp
        fields = '__all__'
        widgets = {
        'studentName': forms.TextInput(attrs={'class': "form-control",'style': 'max-width: 100%; overflow: auto;','placeholder': 'Full Name..'}),
        'studentdep': forms.TextInput(attrs={'class': "form-control",'style': 'max-width: 100%; overflow: auto;','placeholder': 'Department..'}),
        'studentCard': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Your Card Number..'}),
        'studentSnum': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Social Security Number..'}),
        'studenTel': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Your Phone Number..'}),
        'prepDeplome': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Licsense/Master..'}),
        'sprvisorName': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Supervisor full name..'}),}  

    


