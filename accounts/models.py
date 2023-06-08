from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone

User = settings.AUTH_USER_MODEL
# Create your models here.

class User(AbstractUser):
    pass
    def __str__(self):
        return str(self.username)

class VerificationCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)

    def __str__(self):
        return str(self.user)

class University(models.Model):
    name = models.CharField(max_length=6)
    addres = models.CharField(max_length=6)

    def __str__(self):
        return str(self.name)

class Faculty(models.Model):
    univ = models.OneToOneField(University, on_delete=models.CASCADE)
    name = models.CharField(max_length=6)

    def __str__(self):
        return str(self.name)

class Department(models.Model):
    fac = models.OneToOneField(Faculty, on_delete=models.CASCADE)
    name = models.CharField(max_length=6)

    def __str__(self):
        return str(self.name)

class Student(models.Model):
    username = models.OneToOneField(User,null=True,blank=True, on_delete=models.CASCADE,related_name='student')
    approvedAccount = models.BooleanField(max_length=100,null=True,blank=True,default=False)
    verifiedLogin = models.BooleanField(max_length=100,null=True,blank=True,default=False)
    FullName = models.CharField(max_length=100,null=True)
    university = models.CharField(max_length=100,null=True)
    department = models.CharField(max_length=100,null=True)
    studentCard = models.IntegerField(null=True)
    studentSnum = models.IntegerField(null=True)
    studenTel = models.IntegerField(max_length=100,null=True)
    prepDeplome = models.CharField(max_length=100,null=True)
    birthDate= models.DateField(null=True,blank=True)
    birthPlace= models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return str(self.username)

class Admin(models.Model):
    username = models.OneToOneField(User,null=True, blank=True,on_delete=models.CASCADE)
    fullname = models.CharField(max_length=100,null=True)
    dep = models.CharField(max_length=100,null=True)
    university = models.CharField(max_length=100,null=True)

    def __str__(self):
        return str(self.fullname)

class Supervisor(models.Model):
    username = models.OneToOneField(User,null=True,blank=True, on_delete=models.CASCADE,related_name='supervisor')
    fullname = models.CharField(max_length=100,null=True)
    email= models.EmailField(null=True,blank=True)
    Tel = models.IntegerField(null=True)
    Fax = models.IntegerField(null=True)
    password = models.CharField(max_length=100,null=True)

    def __str__(self):
        return str(self.fullname)

class Attendence(models.Model):
    internMaster = models.ForeignKey(User,related_name="sprvor",null=True,blank=True,on_delete= models.SET_NULL)
    intern = models.ForeignKey(User,related_name="user",null=True,blank=True,on_delete= models.SET_NULL)
    prepDeplome = models.CharField(max_length=100,null=True,blank=True)
    companyAdrss = models.CharField(max_length=100,null=True,blank=True)
    strtDate=models.DateField(null=True,blank=True)
    endDate=models.DateField(null=True,blank=True)   
    internshipDay = models.DateField(null=True,blank=True)
    workingHours = models.IntegerField(null=True,blank=True)
    observation = models.CharField(max_length=100,null=True,blank=True)
    isPresent = models.BooleanField(null=True,blank=True) 

    def __str__(self):
        return str(self.internMaster)



class Marks(models.Model):
    internMaster = models.ForeignKey(User,related_name="mster",null=True,blank=True,on_delete= models.SET_NULL)
    intern = models.ForeignKey(User,related_name="intrn",null=True,blank=True,on_delete= models.SET_NULL)
    StudentbirthDate= models.DateField(null=True,blank=True)
    StudentbirthPlace= models.CharField(max_length=100,null=True,blank=True)
    prepDeplome = models.CharField(max_length=100,null=True,blank=True)
    duree = models.CharField(max_length=100,null=True,blank=True)
    strtDate=models.DateField(null=True,blank=True)
    endDate=models.DateField(null=True,blank=True)
    companyName = models.CharField(max_length=100,null=True,blank=True)
    companyAdrss = models.CharField(max_length=100,null=True,blank=True)
    workPlan = models.CharField(max_length=100,null=True)
    gnrlDiscipline = models.IntegerField(null=True)
    workAptitudes = models.IntegerField(null=True)
    initiative = models.IntegerField(null=True)
    innovationAbilities = models.IntegerField(null=True)
    knowledgeAcquired = models.IntegerField(null=True)
    fullMark = models.IntegerField(null=True,blank=True)
    createdDate = models.DateField(default=timezone.now)
    Appreciation = models.CharField(max_length=100,null=True)

    def __str__(self):
        return str(self.internMaster)

class InternOffer(models.Model):
    internMaster = models.ForeignKey(User,related_name="offerspr",null=True,blank=True,on_delete= models.SET_NULL)
    Sprvisorfullname = models.CharField(max_length=100,null=True,blank=True)
    Sprvisoremail= models.EmailField(null=True,blank=True)
    SprvisorTel = models.IntegerField(null=True,blank=True)
    SprvisorFax = models.IntegerField(null=True,blank=True)
    theme = models.CharField(max_length=100,null=True,blank=True)
    duree = models.CharField(max_length=100,null=True,blank=True)
    coverLetter = models.CharField(max_length=100,null=True,blank=True)
    companyName = models.CharField(max_length=100,null=True,blank=True)
    companyAdrss = models.CharField(max_length=100,null=True,blank=True)
    strtDate=models.DateField(null=True,blank=True)
    endDate=models.DateField(null=True,blank=True)   
    Salary = models.IntegerField(null=True,blank=True)

    def __str__(self):
        return str(self.internMaster)

class InternshipApp(models.Model):
    applicant = models.ForeignKey(User,related_name="std",null=True,blank=True,on_delete= models.SET_NULL)
    internMaster = models.ForeignKey(User,related_name="spv",null=True,blank=True,on_delete= models.SET_NULL)
    depMaster = models.ForeignKey(User,related_name="adm",null=True,blank=True,on_delete= models.SET_NULL)
    approvedByMaster= models.BooleanField(null=True,blank=True)
    approvedBySupervisor= models.BooleanField(null=True,blank=True) 
    MasterDefinitelyReject= models.BooleanField(null=True,blank=True) 
    SuprvDefinitelyReject= models.BooleanField(null=True,blank=True) 
    RejectionReason=models.CharField(max_length=100,null=True,blank=True)
    rated = models.BooleanField(null=True,blank=True)

    sprvisorName = models.CharField(max_length=100,null=True,blank=True)
    sprvisorTel = models.IntegerField(null=True)
    sprvisorFax = models.IntegerField(null=True)
    sprvisorEmail = models.EmailField(null=True)
    companyName = models.CharField(max_length=100,null=True)
    companyAdrss = models.CharField(max_length=100,null=True)

    coverLetter = models.CharField(max_length=100,null=True,blank=True)
    studentName = models.CharField(max_length=100,null=True,blank=True)
    studentdep = models.CharField(max_length=100,null=True,blank=True)
    StudentbirthDate= models.DateField(null=True,blank=True)
    StudentbirthPlace= models.CharField(max_length=100,null=True,blank=True)
    studentCard = models.IntegerField(null=True,blank=True)
    studentSnum = models.IntegerField(null=True,blank=True)
    studenTel = models.CharField(max_length=100,null=True,blank=True)
    prepDeplome = models.CharField(max_length=100,null=True,blank=True)

    theme = models.CharField(max_length=100,null=True)
    duree = models.CharField(max_length=100,null=True)
    strtDate=models.DateField(null=True)
    endDate=models.DateField(null=True)
    
    def __str__(self):
        return str(self.applicant)
