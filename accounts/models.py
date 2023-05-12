from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.contrib.auth.models import User

User = settings.AUTH_USER_MODEL
# Create your models here.

class User(AbstractUser):
    pass
    def __str__(self):
        return self.username

class Student(models.Model):
    username = models.CharField(max_length=100,null=True)
    email= models.EmailField(null=True)
    set_password = models.CharField(max_length=100,null=True)
    department = models.CharField(max_length=100,null=True)


class Admin(models.Model):
    fullname = models.CharField(max_length=100,null=True)
    email= models.EmailField(null=True)
    password = models.CharField(max_length=100,null=True)
    dep = models.CharField(max_length=100,null=True)

    def __str__(self):
        return self.fullname

class Supervisor(models.Model):
    fullname = models.CharField(max_length=100,null=True)
    email= models.EmailField(null=True)
    password = models.CharField(max_length=100,null=True)

    def __str__(self):
        return self.fullname

class InternshipApp(models.Model):
    applicant = models.ForeignKey(User,related_name="std",null=True,blank=True,on_delete= models.SET_NULL)
    internMaster = models.ForeignKey(User,related_name="spv",null=True,blank=True,on_delete= models.SET_NULL)
    approvedByMaster= models.BooleanField(null=True,blank=True)
    approvedBySupervisor= models.BooleanField(null=True,blank=True) 
    
    sprvisorName = models.CharField(max_length=100,null=True,blank=True)
    sprvisorTel = models.IntegerField(null=True)
    sprvisorFax = models.IntegerField(null=True)
    sprvisorEmail = models.EmailField(null=True)
    companyName = models.CharField(max_length=100,null=True)
    companyAdrss = models.CharField(max_length=100,null=True)

    studentName = models.CharField(max_length=100,null=True,blank=True)
    studentdep = models.CharField(max_length=100,null=True)
    studentCard = models.IntegerField(null=True)
    studentSnum = models.IntegerField(null=True)
    studenTel = models.CharField(max_length=100,null=True)
    prepDeplome = models.CharField(max_length=100,null=True)

    theme = models.CharField(max_length=100,null=True)
    duree = models.CharField(max_length=100,null=True)
    strtDate=models.DateField(null=True)
    endDate=models.DateField(null=True)
    
    def __str__(self):
        return self.applicant
