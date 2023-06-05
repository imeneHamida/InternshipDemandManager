from django import forms
from django.forms import ModelForm 
from .models import *
from django.forms import ModelForm, TextInput, EmailInput
from django.contrib.auth.password_validation import validate_password
from django.core.validators import EmailValidator, MinLengthValidator
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


class CustomEmailValidator(EmailValidator):
    def __call__(self, value):
        super().__call__(value)
        
        if not value.endswith('@univ-constantine2.dz'):
            raise ValidationError("Email must be in the format example@univ-constantine2.dz.")


class CreationUserForm(forms.Form):
    username = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={"placeholder": "Enter Your Matric Number"}),
        validators=[MinLengthValidator(1, message="Username field is required.")]
    )

    email = forms.EmailField(
        max_length=255,
        widget=forms.EmailInput(attrs={"placeholder": "Enter Your E-mail Address"}),
        validators=[CustomEmailValidator(message="Please enter a valid email address.")]
    )

    password = forms.CharField(
        max_length=255,
        widget=forms.PasswordInput(
            attrs={"placeholder": "Enter Your Password", "id": "password"}
        ),
        validators=[
            MinLengthValidator(8, message="Password must be at least 8 characters."),
            validate_password
        ]
    )

    password2 = forms.CharField(
        max_length=255,
        widget=forms.PasswordInput(
            attrs={"placeholder": "Confirm Your Password", "id": "password2"}
        ),
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password and password2 and password != password2:
            self.add_error("password2", "Passwords do not match.")

        return cleaned_data

 
class CreationIntenApp(ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['required'] = True
    class Meta:
        model = InternshipApp
        fields = '__all__'
        widgets = {
        'studentName': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Your Full name..'}),
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
        

class TakePresence(ModelForm):
    class Meta:
        model = Attendence
        fields = '__all__'
        widgets = {
        'prepDeplome': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Explain Theme of the intenrship..','rows':3, 'cols':5,'style': 'max-width: 100%; Height: 100px;overflow: auto;'}),
        'companyAdrss': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Social Security Number..'}),
        'strtDate': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Social Security Number..'}),
        'endDate': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Social Security Number..'}),
        'internshipDay': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Social Security Number..'}),
        'workingHours': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Social Security Number..'}),
        'observation': forms.Textarea(attrs={'class': 'form-control','placeholder': 'Explain Theme of the intenrship..','rows':3, 'cols':5,'style': 'max-width: 100%; Height: 100px;overflow: auto;'}),
        'isPresent': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Social Security Number..'}),
} 


class Rating(ModelForm):
    class Meta:
        model = Marks
        fields = ['internMaster', 'workPlan', 'gnrlDiscipline', 'workAptitudes', 'initiative', 'innovationAbilities', 'knowledgeAcquired', 'Appreciation']
        widgets = {
        'internMaster': forms.Select(attrs={'class': 'form-control'}),
        'workPlan': forms.Textarea(attrs={'class': 'form-control','placeholder': 'Explain Theme of the intenrship..','rows':3, 'cols':5,'style': 'max-width: 100%; Height: 100px;overflow: auto;'}),
        'gnrlDiscipline': forms.NumberInput(attrs={'class': 'form-control','placeholder': 'Rate out of /4..','min': 0,'max': 4,'step': 1}),
        'workAptitudes': forms.NumberInput(attrs={'class': 'form-control','placeholder': 'Rate out of /4..','min': 0,'max': 4,'step': 1}),
        'initiative': forms.NumberInput(attrs={'class': 'form-control','placeholder': 'Rate out of /4..','min': 0,'max': 4,'step': 1}),
        'innovationAbilities': forms.NumberInput(attrs={'class': 'form-control','placeholder': 'Rate out of /4..','min': 0,'max': 4,'step': 1}),
        'knowledgeAcquired': forms.NumberInput(attrs={'class': 'form-control','placeholder': 'Rate out of /4..','min': 0,'max': 4,'step': 1}),
        'Appreciation': forms.Textarea(attrs={'class': 'form-control','placeholder': 'Write Overall Appreciation..','rows':3, 'cols':5,'style': 'max-width: 100%; Height: 100px;overflow: auto;'}),} 


class StudentEditProfile(ModelForm):
    PREP_DEPLOME_CHOICES = [
        ('license', 'License'),
        ('master', 'Master'),
    ]
    DEPARTMENT_CHOICES = [
        ('ifa', 'IFA'),
        ('tlsi', 'TLSI'),
    ]
    UNIV = [
        ('University Constantine 2', 'University Constantine 2'),
    ]
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter new password'}), required=False)
    prepDeplome = forms.ChoiceField(choices=PREP_DEPLOME_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))   
    department = forms.ChoiceField(choices=DEPARTMENT_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    university = forms.ChoiceField(choices=UNIV, widget=forms.Select(attrs={'class': 'form-control'}))   
    class Meta:
        model = Student
        fields = '__all__'
        widgets = {
        'username': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Type you correct full name..'}),
        'FullName': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Type you correct full name..'}),
        'studentCard': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Student Card Number..'}),
        'studentSnum': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Social Security Number..'}),
        'studenTel': forms.TextInput(attrs={'class': 'form-control','placeholder': '### ### ### ###'}),
} 


class SupervisorEditProfile(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter new password'}), required=False)
    class Meta:
        model = Supervisor
        fields = '__all__'
        widgets = {
        'username': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Type you correct full name..'}),
        'fullname': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Type you correct full name..'}),
        'Tel': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Student Card Number..'}),
        'Fax': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Social Security Number..'}),} 


class AdminEditProfile(ModelForm):
    DEPARTMENT_CHOICES = [
    ('ifa', 'IFA'),
    ('tlsi', 'TLSI'),]

    UNIV = [
    ('University Constantine 2', 'University Constantine 2'),]
    university = forms.ChoiceField(choices=UNIV, widget=forms.Select(attrs={'class': 'form-control'}))      
    dep = forms.ChoiceField(choices=DEPARTMENT_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter new password'}), required=False)
    class Meta:
        model = Admin
        fields = '__all__'
        widgets = {
        'username': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Type you correct full name..'}),
        'fullname': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Type you correct full name..'}),} 