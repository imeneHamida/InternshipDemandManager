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
    path('Deleteaccount/', views.delete_account ,name="deleteAccount"),
    #path('StudentInfo/<str:pk>/', views.StudentInfo ,name="StudentInfo"),
    path('logout/', views.LogoutUser ,name="LogoutUser"),
    path('CreateOffer/', views.CreateOffer ,name="CreateOffer"),
    path('EditOffer/<str:pk>/', views.EditOffer ,name="EditOffer"),
    path('ApplyForOffer/<str:pk>/', views.ApplyForOffer ,name="ApplyForOffer"),
    path('Signup/', views.Signup ,name="Signup"),
    path('student-home/', views.StudentHome, name='StudentHome'),
    path('StudentProfile/', views.StudentProfile ,name="StudentProfile"),
    path('SupervisorProfile/', views.SupervisorProfile ,name="SupervisorProfile"),
    path('AdminProfile/', views.AdminProfile ,name="AdminProfile"),
    path('EditStudentProfile/', views.studentEditProfile ,name="EditStudentProfile"),
    path('MyApplications/', views.MyApplications ,name="MyApplications"),
    path('InternOffers/', views.InternOffers ,name="InternOffers"),
    path('AdminHome/', views.AdminHome ,name="AdminHome"),
    path('SupervisorHome/', views.SupervisorHome ,name="SupervisorHome"),
    path('Applications/', views.Applications ,name="Applications"),
    path('Aboutus/', views.Aboutus ,name="Aboutus"),
    path('internappform/', views.internappform ,name="internappform"),
    path('CreateAdmin/', views.CreateAdmin, name="CreateAdmin"),
    path('CreateSupervisor/', views.CreateSupervisor, name="CreateSupervisor"),
    path('ApprovedByAdmin/<str:pk>/', views.ApprovedByAdmin, name='ApprovedByAdmin'),
    path('DeclinedByAdmin/<str:pk>/', views.DeclinedByAdmin, name='DeclinedByAdmin'),
    path('ApprovedBySupervisor/<str:pk>/', views.ApprovedBySupervisor, name='ApprovedBySupervisor'),
    path('DeclinedBySupervisor/<str:pk>/', views.DeclinedBySupervisor, name='DeclinedBySupervisor'),
    path('DefinitelyRejectByAdmin/<str:pk>/', views.DefinitelyRejectByAdmin, name='DefinitelyRejectByAdmin'),
    path('DefinitelyRejectBySupervisor/<str:pk>/', views.DefinitelyRejectBySupervisor, name='DefinitelyRejectBySupervisor'),
    path('updateApplication/<str:pk>/', views.updateApp, name='updateApp'),
    path('DeleteApp/<str:pk>/', views.DeleteApp, name='DeleteApp'),
    path('StudentRating/<str:pk>/', views.StudentRating, name='StudentRating'),
    path('InternIspresent/<str:pk>/', views.InternIspresent, name='InternIspresent'),
    path('InternIsNotpresent/<str:pk>/', views.InternIsNotpresent, name='InternIsNotpresent'),
    path('viewRating/<str:pk>/', views.viewRating, name='viewRating'),
    path('InternshipCertificate/<str:pk>/', views.render_to_pdf, name='Certificate'),
    path('InternshipAgreement/<str:pk>/', views.PrintAgreement, name='PrintAgreement'),
    ]
