from .forms import CreationUserForm,CreationIntenApp,Rating,TakePresence
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView
from .decorators import admin_redirect,unauthenticated_user,allowed_users
from django.contrib.auth.models import Group
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User
from .email_utils import send_account_details_email
from django.conf import settings
from .utils import render_to_pdf
from django.contrib.auth import authenticate,login,logout
from .models import *
from django.views import View
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa 

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
    send_account_details_email(supemail, supusername, suppassword)
    apps = InternshipApp.objects.all()
    return render(request,"AdminHome.html",{'appslist' : apps})

@allowed_users(allowed_roles=['admin'])
@login_required(login_url='Signin')
def DeclinedByAdmin(request, pk):
    app = InternshipApp.objects.get(id=pk)
    app.approvedByMaster = False
    app.RejectionReason = request.POST.get("RejectionReason")
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

def render_to_pdf(request, pk):
    app = InternshipApp.objects.get(id=pk)
    marks = Marks.objects.filter(intern= app.applicant)
    template = get_template('Certificate.html')
    context = {'marks': marks} 
    html = template.render(context)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)

    # Checking if PDF generation was successful
    if not pdf.err:
        # Set the appropriate response headers for PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="Certification.pdf"'
        # Write the PDF file to the response
        response.write(result.getvalue())
        return response
    # Return an error response if PDF generation failed
    return HttpResponse('Error generating PDF', status=500)

#class Certificate(View):
    #def get(self, request, *args, **kwargs):
        #pdf = render_to_pdf('Certificate.html')
        #return HttpResponse(pdf, content_type='application/pdf')

@allowed_users(allowed_roles=['Supervisor'])
@login_required(login_url='Signin')
def StudentRating(request, pk):
    app = InternshipApp.objects.get(id=pk)
    appintern = app.applicant 
    form = Rating()
    if request.method =='POST':
        form = Rating(request.POST)
        if form.is_valid():
            marks_instance = form.save(commit=False)
            marks_instance.internMaster = request.user
            marks_instance.intern = appintern
            marks_instance.prepDeplome = app.prepDeplome
            marks_instance.duree = app.duree
            marks_instance.strtDate = app.strtDate
            marks_instance.endDate = app.endDate
            marks_instance.companyName = app.companyName
            marks_instance.companyAdrss = app.companyAdrss
            app.rated = True
            app.save()
            marks_instance.save()
            return redirect('SupervisorHome')
    context = {'form': form}
    return render(request,"Marks.html", context)


@allowed_users(allowed_roles=['Supervisor','univStudents'])
@login_required(login_url='Signin')
def viewRating(request, pk):
    app = InternshipApp.objects.get(id=pk)
    appintern = app.applicant
    marks = Marks.objects.filter(intern=app.applicant)
    
    supervisor_group = Group.objects.get(name='Supervisor')
    
    if supervisor_group in request.user.groups.all():
        template = "SupervisorHome.html"
    else:
        template = "MyApplications.html"
    
    context = {'marks': marks}
    return render(request, template, context)

@allowed_users(allowed_roles=['Supervisor'])
@login_required(login_url='Signin')
def InternIspresent(request, pk):
    app = InternshipApp.objects.get(id=pk)
    appintern = app.applicant 
    supervsr = request.user
    prepDeplome = app.prepDeplome
    companyAdrss = app.companyAdrss
    strtDate = app.strtDate
    endDate = app.endDate
    if request.method =='POST':
        attendance = Attendence.objects.create(internMaster = supervsr,
        intern = appintern,
        prepDeplome = prepDeplome,
        companyAdrss = companyAdrss,
        strtDate = strtDate,
        endDate = endDate
        )
        attendance.isPresent = True
        attendance.internshipDay = request.POST.get("internshipDay")
        attendance.workingHours = request.POST.get("workingHours")
        attendance.observation = request.POST.get("internshipDay")
        attendance.save()
        return redirect('SupervisorHome')
    apps = InternshipApp.objects.all()
    return render(request,"SupervisorHome.html",{'appslist' : apps})

@allowed_users(allowed_roles=['Supervisor'])
@login_required(login_url='Signin')
def InternIsNotpresent(request, pk):
    app = InternshipApp.objects.get(id=pk)
    appintern = app.applicant 
    supervsr = request.user
    prepDeplome = app.prepDeplome
    companyAdrss = app.companyAdrss
    strtDate = app.strtDate
    endDate = app.endDate
    if request.method =='POST':
        attendance = Attendence.objects.create(internMaster = supervsr,
        intern = appintern,
        prepDeplome = prepDeplome,
        companyAdrss = companyAdrss,
        strtDate = strtDate,
        endDate = endDate
        )
        attendance.isPresent = False
        attendance.internshipDay = request.POST.get("internshipDay")
        attendance.workingHours = request.POST.get("workingHours")
        attendance.observation = request.POST.get("observation")
        attendance.save()
        return redirect('SupervisorHome')
    apps = InternshipApp.objects.all()
    return render(request,"SupervisorHome.html",{'appslist' : apps})

@allowed_users(allowed_roles=['Supervisor'])
@login_required(login_url='Signin')
def DefinitelyRejectBySupervisor(request, pk):
    app = InternshipApp.objects.get(id=pk)
    app.SuprvDefinitelyReject = True
    app.save()
    apps = InternshipApp.objects.all()
    return render(request,"SupervisorHome.html",{'appslist' : apps})

@allowed_users(allowed_roles=['admin'])
@login_required(login_url='Signin')
def DefinitelyRejectByAdmin(request, pk):
    app = InternshipApp.objects.get(id=pk)
    app.MasterDefinitelyReject = True
    app.save()
    apps = InternshipApp.objects.all()
    return render(request,"AdminHome.html",{'appslist' : apps})

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
    total = supervisors.count()
    return render(request,"SupervisorHome.html",{'appslist' : supervisors ,'total_apps' : total})

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
    Details = request.user.Student.objects.all
    context = { 'Details': Details }
    return render(request,"StudentProfile.html", context)

@login_required(login_url='Signin')
@allowed_users(allowed_roles=['univStudents'])
def MyApplications(request):
    apps = InternshipApp.objects.filter(applicant = request.user)
    total_apps = apps.count()
    marks = Marks.objects.filter(intern= request.user)
    return render(request,"MyApplications.html", { 'myapps': apps , 'total_apps': total_apps, 'marks': marks})



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
            Student.objects.create(username=user)
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
            #your_model_instance = InternshipApp(internMaster=user)--the right thing to do instead is to write:
            #InternshipApp.objects.create(internMaster=user)
            #your_model_instance.save()--to remove
            messages.success(request, "Account Created successfully")
    context = {'form': form }
    return render(request, "CreateSupervisor.html", context)