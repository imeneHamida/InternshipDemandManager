from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.contrib.auth.models import User

User = settings.AUTH_USER_MODEL
# Create your models here.

class User(AbstractUser):
    pass
    def __str__(self):
        return str(self.username)

class Student(models.Model):
    username = models.OneToOneField(User,null=True, on_delete=models.CASCADE)
    firstName = models.CharField(max_length=100,null=True)
    lastName = models.CharField(max_length=100,null=True)
    university = models.CharField(max_length=100,null=True)
    department = models.CharField(max_length=100,null=True)
    studentCard = models.IntegerField(null=True)
    studentSnum = models.IntegerField(null=True)
    studenTel = models.CharField(max_length=100,null=True)
    prepDeplome = models.CharField(max_length=100,null=True)

    def __str__(self):
        return str(self.username)

class Admin(models.Model):
    fullname = models.CharField(max_length=100,null=True)
    email= models.EmailField(null=True)
    password = models.CharField(max_length=100,null=True)
    dep = models.CharField(max_length=100,null=True)

    def __str__(self):
        return str(self.fullname)

class Supervisor(models.Model):
    fullname = models.CharField(max_length=100,null=True)
    email= models.EmailField(null=True)
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
    #studentBirthDate
    #studentBirthPlace
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
    #Date: Currentdate
    Appreciation = models.CharField(max_length=100,null=True)

    def __str__(self):
        return str(self.internMaster)


class InternshipApp(models.Model):
    applicant = models.ForeignKey(User,related_name="std",null=True,blank=True,on_delete= models.SET_NULL)
    internMaster = models.ForeignKey(User,related_name="spv",null=True,blank=True,on_delete= models.SET_NULL)
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

    studentName = models.CharField(max_length=100,null=True,blank=True)
    studentdep = models.CharField(max_length=100,null=True)
    #studentBirthDate
    #studentBirthPlace  
    studentCard = models.IntegerField(null=True)
    studentSnum = models.IntegerField(null=True)
    studenTel = models.CharField(max_length=100,null=True)
    prepDeplome = models.CharField(max_length=100,null=True)

    theme = models.CharField(max_length=100,null=True)
    duree = models.CharField(max_length=100,null=True)
    strtDate=models.DateField(null=True)
    endDate=models.DateField(null=True)
    
    def __str__(self):
        return str(self.applicant)
