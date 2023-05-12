from .forms import CreationUserForm,CreationIntenApp
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView
from .decorators import admin_redirect,unauthenticated_user,allowed_users
from django.contrib.auth.models import Group
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User
from .email_utils import send_account_details_email
from django.contrib.auth import authenticate,login,logout
from .models import *

# Create your views here.

def alertView(request):
    message = "This is an alert message!"
    return render(request, 'Alertdialog.html', {'message': message})


@unauthenticated_user
def Home(request):
    context = { }
    return render(request, "Home.html", context)

#def StudentInfo(request, pk):
    #studentinfo = Student.objects.get(id=pk)
    #context = {'studentinfo': studentinfo}
    #return render(request, "StudentInfo.html", context)

@unauthenticated_user
def Aboutus(request):
    context = { }
    return render(request, "AboutUs.html", context)


@allowed_users(allowed_roles=['univStudents'])
@login_required(login_url='Signin')
class UpdateView(UpdateView):
   model=Student
   fields="__all__"
   template_name='internAppForm.html'
   success_url='/internappform/'
def updateApp(request, pk):
    Myapp = InternshipApp.objects.get(id=pk)
    return render(request,"internAppForm.html", context)

@login_required(login_url='Signin')
@allowed_users(allowed_roles=['univStudents'])
def DeleteApp(request, pk):
    myapps = InternshipApp.objects.filter(applicant = request.user)
    deleteapp = InternshipApp.objects.get(id=pk)
    deleteapp.delete()
    return render(request,"MyApplications.html", { 'myapps': myapps , 'deleteapp': deleteapp})


@allowed_users(allowed_roles=['admin'])
@login_required(login_url='Signin')
def ApprovedByAdmin(request, pk):
    app = InternshipApp.objects.get(id=pk)
    app.approvedByMaster = True
    app.save()
    supusername = app.sprvisorName
    suppassword = 'iamsupervisor'
    supemail = app.sprvisorEmail
    user = User.objects.create_user(
        username= supusername,
        email= supemail,
        password= suppassword,
    )
    user.save()
    supervisor_group = Group.objects.get(name='Supervisor') 
    user.groups.add(supervisor_group)
    Supervisor.objects.create(fullname=supusername,email=supemail,password=suppassword)
    app.internMaster = user
    app.save()
    send_account_details_email(user.email, user.username, user.password)
    apps = InternshipApp.objects.all()
    return render(request,"AdminHome.html",{'appslist' : apps})

#@allowed_users(allowed_roles=['admin'])
@login_required(login_url='Signin')
def DeclinedByAdmin(request, pk):
    app = InternshipApp.objects.get(id=pk)
    app.approvedByMaster = False
    app.save()
    apps = InternshipApp.objects.all()
    return render(request,"AdminHome.html",{'appslist' : apps})

@allowed_users(allowed_roles=['Supervisor'])
@login_required(login_url='Signin')
def ApprovedBySupervisor(request, pk):
    app = InternshipApp.objects.get(id=pk)
    app.approvedBySupervisor = True
    app.save()
    apps = InternshipApp.objects.all()
    return render(request,"SupervisorHome.html",{'appslist' : apps})

@allowed_users(allowed_roles=['Supervisor'])
@login_required(login_url='Signin')
def DeclinedBySupervisor(request, pk):
    app = InternshipApp.objects.get(id=pk)
    app.approvedBySupervisor = False
    app.save()
    apps = InternshipApp.objects.all()
    return render(request,"SupervisorHome.html",{'appslist' : apps})

@login_required(login_url='Signin')
@allowed_users(allowed_roles=['admin'])
def AdminHome(request):
    apps = InternshipApp.objects.all()
    total_apps = apps.count()
    return render(request,"AdminHome.html",{'appslist' : apps,'total_apps': total_apps })

@allowed_users(allowed_roles=['Supervisor'])
@login_required(login_url='Signin')
def SupervisorHome(request):
    supervisors = InternshipApp.objects.filter(internMaster = request.user)
    return render(request,"SupervisorHome.html",{'appslist' : supervisors})

@allowed_users(allowed_roles=['univStudents'])
@login_required(login_url='Signin')
def internappform(request):
    form = CreationIntenApp()
    if request.method =='POST':
        form = CreationIntenApp(request.POST)
        if form.is_valid():
            form.save()
            return redirect('MyApplications')
    context = {'form': form}
    return render(request,"internAppForm.html", context)

@admin_redirect
@login_required(login_url='Signin')
@allowed_users(allowed_roles=['univStudents'])
def StudentHome(request):
    context = { }
    return render(request,"StudentHome.html", context)

@login_required(login_url='Signin')
@allowed_users(allowed_roles=['univStudents'])
def StudentProfile(request):
    context = { }
    return render(request,"StudentProfile.html", context)

@login_required(login_url='Signin')
@allowed_users(allowed_roles=['univStudents'])
def MyApplications(request):
    apps = InternshipApp.objects.filter(applicant = request.user)
    total_apps = apps.count()
    return render(request,"MyApplications.html", { 'myapps': apps , 'total_apps': total_apps})


def LogoutUser(request):
    logout(request)
    context = { }
    return render(request, "Home.html", context)


@unauthenticated_user
def Signin(request):
        if request.method =='POST':
            username = request.POST.get('fullname')
            email = request.POST.get('email')
            password = request.POST.get('password')

            user = authenticate(request, username=username,email=email, password=password)

            if user is not None:
                login(request,user)
                return redirect('StudentHome')
                messages.success(request,'successfuly logged in')
            else:
                messages.info(request,'not correct')
                
        context = { }
        return render(request, "SignIn.html", context)

@unauthenticated_user
def Signup(request):
    form = CreationUserForm()
    if request.method == 'POST':
        form = CreationUserForm(request.POST)
        if form.is_valid():
            username = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")
            password2 = request.POST.get("password2")

            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
            )
            user.save()
            Student_group = Group.objects.get(name='univStudents') 
            user.groups.add(Student_group)
            Student.objects.create(username=user,email=email,set_password=password)
            login(request, user)
            return redirect('Signin')
            messages.success(request, "Account Created successfully")
    context = {'form': form }
    return render(request, "SignUp.html", context)

@allowed_users(allowed_roles=['admin'])
@login_required(login_url='Signin')
def CreateAdmin(request):
    form = CreationUserForm()
    if request.method == 'POST':
        form = CreationUserForm(request.POST)
        if form.is_valid():
            username = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")
            password2 = request.POST.get("password2")

            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
            )
            user.save()
            Admin_group = Group.objects.get(name='admin') 
            user.groups.add(Admin_group)
            Admin.objects.create(fullname=user,)
            messages.success(request, "Account Created successfully")
    context = {'form': form }
    return render(request, "CreateAdminPage.html", context)

@allowed_users(allowed_roles=['admin'])
@login_required(login_url='Signin')
def CreateSupervisor(request):
    form = CreationUserForm()
    if request.method == 'POST':
        form = CreationUserForm(request.POST)
        if form.is_valid():
            username = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")
            password2 = request.POST.get("password2")

            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
            )
            user.save()
            supervisor_group = Group.objects.get(name='Supervisor') 
            user.groups.add(supervisor_group)
            Supervisor.objects.create(fullname=user,email=email,password=password)
            your_model_instance = InternshipApp(internMaster=user)
            your_model_instance.save()
            messages.success(request, "Account Created successfully")
    context = {'form': form }
    return render(request, "CreateSupervisor.html", context)