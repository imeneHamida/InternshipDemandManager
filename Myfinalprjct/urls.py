"""
URL configuration for Myfinalprjct project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from accounts.views import *
from accounts import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Home ,name="Home"),
    path('Signin/', views.Signin ,name="Signin"),
    #path('StudentInfo/<str:pk>/', views.StudentInfo ,name="StudentInfo"),
    path('logout/', views.LogoutUser ,name="LogoutUser"),
    path('Signup/', views.Signup ,name="Signup"),
    path('StudentHome/', views.StudentHome ,name="StudentHome"),
    path('StudentProfile/', views.StudentProfile ,name="StudentProfile"),
    path('MyApplications/', views.MyApplications ,name="MyApplications"),
    path('AdminHome/', views.AdminHome ,name="AdminHome"),
    path('SupervisorHome/', views.SupervisorHome ,name="SupervisorHome"),
    path('Aboutus/', views.Aboutus ,name="Aboutus"),
    path('internappform/', views.internappform ,name="internappform"),
    path('CreateAdmin/', views.CreateAdmin, name="CreateAdmin"),
    path('CreateSupervisor/', views.CreateSupervisor, name="CreateSupervisor"),
    path('ApprovedByAdmin/<str:pk>/', views.ApprovedByAdmin, name='ApprovedByAdmin'),
    path('DeclinedByAdmin/<str:pk>/', views.DeclinedByAdmin, name='DeclinedByAdmin'),
    path('ApprovedBySupervisor/<str:pk>/', views.ApprovedBySupervisor, name='ApprovedBySupervisor'),
    path('DeclinedBySupervisor/<str:pk>/', views.DeclinedBySupervisor, name='DeclinedBySupervisor'),
    path('updateApplication/<str:pk>/', views.updateApp, name='updateApp'),
    path('DeleteApp/<str:pk>/', views.DeleteApp, name='DeleteApp'),
    ]
