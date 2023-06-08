from .forms import *
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView
from .decorators import admin_redirect,unauthenticated_user,allowed_users
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .email_utils import send_account_details_email
from django.conf import settings
from .utils import render_to_pdf
from django.contrib.auth import authenticate,login,logout
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
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

@login_required(login_url='Signin')
def delete_account(request):
    if request.method == 'POST':
        request.user.delete()
        logout(request)
        return redirect('Home')
    return render(request, 'Home.html')

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

@unauthenticated_user
def HowItWorks(request):
    context = { }
    return render(request, "HowItWorks.html", context)


@allowed_users(allowed_roles=['univStudents'])
@login_required(login_url='Signin')
def updateApp(request, pk):
    student = get_object_or_404(InternshipApp, pk=pk, applicant=request.user)
    if request.method == 'POST':
        form = CreationIntenApp(request.POST, instance=student)
        if form.is_valid():
            form.instance.applicant = request.user
            form.instance.studenTel = request.user.student.studenTel
            form.instance.studentCard = request.user.student.studentCard
            form.instance.studentdep = request.user.student.department
            form.instance.studentSnum = request.user.student.studentSnum
            form.instance.prepDeplome = request.user.student.prepDeplome
            form.save()
            return redirect('MyApplications')
    else:
        form = CreationIntenApp(instance=student)

    context = {'form': form}
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

    # Check if the supusername already exists
    if not User.objects.filter(username=supusername).exists():
        user = User.objects.create_user(
            username=supusername,
            email=supemail,
            password=suppassword,
        )
        user.save()
        supervisor_group = Group.objects.get(name='Supervisor') 
        user.groups.add(supervisor_group)
        Supervisor.objects.create(username=user, email=supemail, password=suppassword)
        app.internMaster = user
        app.save()
        send_account_details_email(supemail, supusername, suppassword)

    apps = InternshipApp.objects.filter(studentdep=request.user.admin.dep)
    return render(request, "AdminHome.html", {'appslist': apps})

@allowed_users(allowed_roles=['admin'])
@login_required(login_url='Signin')
def DeclinedByAdmin(request, pk):
    app = InternshipApp.objects.get(id=pk)
    app.approvedByMaster = False
    app.RejectionReason = request.POST.get("RejectionReason")
    app.save()
    apps = InternshipApp.objects.filter(studentdep=request.user.admin.dep)
    return render(request,"AdminHome.html",{'appslist' : apps})

@allowed_users(allowed_roles=['Supervisor'])
@login_required(login_url='Signin')
def ApprovedBySupervisor(request, pk):
    app = InternshipApp.objects.get(id=pk)
    app.approvedBySupervisor = True
    app.save()
    apps = InternshipApp.objects.all()
    return render(request,"SupervisorHome.html",{'appslist' : apps})

@login_required(login_url='Signin')
def ViewPresence(request, pk):
    supervisors = InternshipApp.objects.filter(internMaster = request.user)
    app = InternshipApp.objects.get(id=pk)
    attendence = Attendence.objects.filter(intern=app.applicant,internMaster=app.internMaster)
    return render(request,"viewnpresence.html",{'app' : app,'applist' : supervisors, 'attendence': attendence})

@allowed_users(allowed_roles=['admin','univStudents'])
@login_required(login_url='Signin')
def ViewMarks(request, pk):
    supervisors = InternshipApp.objects.filter(internMaster = request.user)
    app = InternshipApp.objects.get(id=pk)
    marks = Marks.objects.filter(intern=app.applicant,internMaster=app.internMaster)
    return render(request,"viewMarks.html",{'app' : app,'applist' : supervisors, 'marks': marks})

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
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="Certification.pdf"'
        # Writing the PDF file to the response
        response.write(result.getvalue())
        return response
    # Returning an error response if PDF generation failed
    return HttpResponse('Error generating PDF', status=500)

#class Certificate(View):
    #def get(self, request, *args, **kwargs):
        #pdf = render_to_pdf('Certificate.html')
        #return HttpResponse(pdf, content_type='application/pdf')

def PrintAgreement(request, pk):
    app = InternshipApp.objects.get(id=pk)
    template = get_template('Convention.html')
    context = {'app': app} 
    html = template.render(context)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    # Checking if PDF generation was successful
    if not pdf.err:
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="internshipAgreement.pdf"'
        # Writing the PDF file to the response
        response.write(result.getvalue())
        return response
    # Returning an error response if PDF generation failed
    return HttpResponse('Error generating PDF', status=500)

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
            marks_instance.fullMark = (
                form.cleaned_data['gnrlDiscipline']
                + form.cleaned_data['workAptitudes']
                + form.cleaned_data['initiative']
                + form.cleaned_data['innovationAbilities']
                + form.cleaned_data['knowledgeAcquired']
            )
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
        attendance.observation = request.POST.get("observation")
        attendance.save()
        return redirect('Applications')
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
    app.RejectionReason = request.POST.get("RejectionReason")
    app.save()
    apps = InternshipApp.objects.all()
    return render(request,"SupervisorHome.html",{'appslist' : apps})

@allowed_users(allowed_roles=['admin'])
@login_required(login_url='Signin')
def DefinitelyRejectByAdmin(request, pk):
    app = InternshipApp.objects.get(id=pk)
    app.MasterDefinitelyReject = True
    app.RejectionReason = request.POST.get("RejectionReason")
    app.save()
    apps = InternshipApp.objects.filter(studentdep=request.user.admin.dep)
    return render(request,"AdminHome.html",{'appslist' : apps})

@allowed_users(allowed_roles=['Supervisor'])
@login_required(login_url='Signin')
def DeclinedBySupervisor(request, pk):
    app = InternshipApp.objects.get(id=pk)
    app.approvedBySupervisor = False
    app.RejectionReason = request.POST.get("RejectionReason")
    app.save()
    apps = InternshipApp.objects.all()
    return render(request,"SupervisorHome.html",{'appslist' : apps})

@login_required(login_url='Signin')
@allowed_users(allowed_roles=['admin'])
def AdminHome(request):
    apps = InternshipApp.objects.filter(studentdep=request.user.admin.dep)
    total_apps = apps.count()
    admin = InternshipApp.objects.filter(depMaster = request.user)
    attendence = Attendence.objects.filter(intern__in=admin.values('applicant'))
    marks = Marks.objects.filter(intern__in=admin.values('applicant'))
    return render(request,"AdminHome.html",{'appslist' : apps,'total_apps': total_apps, 'attendence': attendence ,'marks': marks})

@login_required(login_url='Signin')
@allowed_users(allowed_roles=['admin'])
def ViewNewAccounts(request):
    accounts = Student.objects.filter(approvedAccount = False)
    total_accounts = accounts.count()
    return render(request,"NewAccounts.html",{'accountslist' : accounts,'total_accounts': total_accounts})

@login_required(login_url='Signin')
@allowed_users(allowed_roles=['admin'])
def ApproveAccount(request, pk):
    accounts = Student.objects.filter(approvedAccount = False)
    total_accounts = accounts.count()
    student = Student.objects.get(id=pk)
    email = student.username.email
    if request.method == 'POST':
        verification_code = get_random_string(length=6)
        verification_obj = VerificationCode(user=student.username, code=verification_code)
        verification_obj.save()
        send_mail(
        'Account Verification',
        f'Your verification code is: {verification_code}',
        'imene.hamida18@gmail.com',
        [email],
        fail_silently=False,
        )
        student.approvedAccount = True
        student.save()
    return render(request,"NewAccounts.html",{'accountslist' : accounts,'total_accounts': total_accounts})


@login_required(login_url='Signin')
@allowed_users(allowed_roles=['admin'])
def AdminProfile(request):
    Admin = request.user.admin
    if request.method == 'POST':
        form = AdminEditProfile(request.POST, instance=Admin)
        if form.is_valid():
            Admin.username = request.user 
            submmitedform = form.save(commit=False)
            password = form.cleaned_data.get('password')
            if password:
                # Setting the new password for the user
                request.user.set_password(password)
                request.user.save()
            Admin.save()
            return redirect('AdminProfile')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = AdminEditProfile(instance=Admin)
    context = {'form': form}
    return render(request, 'AdminProfile.html', context)

@allowed_users(allowed_roles=['Supervisor'])
@login_required(login_url='Signin')
def SupervisorHome(request):
    offers = InternOffer.objects.filter(internMaster = request.user)
    total_offers = offers.count()
    return render(request,"SupervisorHome.html",{'offers' : offers, 'total_offers': total_offers})

@allowed_users(allowed_roles=['Supervisor'])
@login_required(login_url='Signin')
def CreateOffer(request):
    if request.method == 'POST':
        form = CreateOfferForm(request.POST)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.internMaster = request.user
            offer.Sprvisorfullname = request.user.supervisor.fullname
            offer.Sprvisoremail = request.user.supervisor.email
            offer.SprvisorTel = request.user.supervisor.Tel
            offer.SprvisorFax = request.user.supervisor.Fax
            offer.save()
            return redirect('SupervisorHome')
    else:
        form = CreateOfferForm()
        error_message = 'unvalid data'
    
    context = {'form': form}
    return render(request, "CreateOffer.html", context)

@allowed_users(allowed_roles=['Supervisor'])
@login_required(login_url='Signin')
def EditOffer(request, pk):
    offer = get_object_or_404(InternOffer, pk=pk, internMaster=request.user)
    if request.method == 'POST':
        form = CreateOfferForm(request.POST, instance=offer)
        if form.is_valid():
            starting_date = form.cleaned_data['strtDate']
            ending_date = form.cleaned_data['endDate']
            
            if starting_date > ending_date:
                error_message = 'Starting date cannot be later than the ending date.'
                context = {'error_message': error_message, 'offer': offer, 'form': form}
                return render(request, 'CreateOffer.html', context)
            else:
                form.instance.internMaster = request.user
                form.instance.Sprvisorfullname = request.user.supervisor.fullname
                form.instance.Sprvisoremail = request.user.supervisor.email
                form.instance.SprvisorTel = request.user.supervisor.Tel
                form.instance.SprvisorFax = request.user.supervisor.Fax
                form.instance.save()
                return redirect('SupervisorHome')
    else:
        form = CreateOfferForm(instance=offer)
    
    context = {'offer': offer, 'form': form}
    return render(request, "CreateOffer.html", context)


@allowed_users(allowed_roles=['Supervisor'])
@login_required(login_url='Signin')
def Applications(request):
    supervisors = InternshipApp.objects.filter(internMaster = request.user,approvedByMaster= True)
    attendence = Attendence.objects.filter(intern__in=supervisors.values('applicant'))
    total = supervisors.count()
    return render(request,"Applications.html",{'appslist' : supervisors ,'total_apps' : total, 'attendence': attendence})


@allowed_users(allowed_roles=['Supervisor'])
@login_required(login_url='Signin')
def SupervisorProfile(request):
    supervisor = request.user.supervisor
    if request.method == 'POST':
        form = SupervisorEditProfile(request.POST, instance=supervisor)
        if form.is_valid():
            supervisor.username = request.user 
            submmitedform = form.save(commit=False)
            password = form.cleaned_data.get('password')
            if password:
                # Setting the new password for the user
                request.user.set_password(password)
                request.user.save()
            supervisor.save()
            return redirect('SupervisorProfile')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = SupervisorEditProfile(instance=supervisor)
    context = {'form': form}
    return render(request, 'SupervisorProfile.html', context)

@allowed_users(allowed_roles=['univStudents'])
@login_required(login_url='Signin')
def InternOffers(request):
    offers = InternOffer.objects.all()
    app = InternshipApp.objects.all()
    total = offers.count()
    return render(request,"InternOffers.html",{'offers' : offers ,'total_offers' : total , 'app': app})

@allowed_users(allowed_roles=['univStudents'])
@login_required(login_url='Signin')
def internappform(request):
    if request.method == 'POST':
        form = CreationIntenApp(request.POST)
        if form.is_valid():
            form.instance.applicant = request.user
            form.instance.studenTel = request.user.student.studenTel
            form.instance.studentCard = request.user.student.studentCard
            form.instance.studentdep = request.user.student.department
            form.instance.studentSnum = request.user.student.studentSnum
            form.instance.prepDeplome = request.user.student.prepDeplome
            form.save()
            return redirect('MyApplications')
    else:
        form = CreationIntenApp()

    context = {'form': form}
    return render(request, 'internAppForm.html', context)

@unauthenticated_user
def contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        send_mail(
            subject,
            f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}",
            settings.DEFAULT_FROM_EMAIL,
            [settings.DEFAULT_FROM_EMAIL],
            fail_silently=False,
        )

    return render(request, 'Home.html') 

@allowed_users(allowed_roles=['univStudents'])
@login_required(login_url='Signin')
def ApplyForOffer(request, pk):
    offer = get_object_or_404(InternOffer, pk=pk)
    offers = InternOffer.objects.all()
    total = offers.count()
    if request.method == 'POST':
        app = InternshipApp.objects.create(applicant = request.user)
        app.internMaster = offer.internMaster
        app.studenTel = request.user.student.studenTel
        app.studentCard = request.user.student.studentCard
        app.studentdep = request.user.student.department
        app.studentSnum = request.user.student.studentSnum
        app.prepDeplome = request.user.student.prepDeplome
        app.coverLetter = offer.coverLetter
        app.companyName = offer.companyName
        app.companyAdrss = offer.companyAdrss
        app.sprvisorName = offer.Sprvisorfullname
        app.sprvisorEmail = offer.Sprvisoremail
        app.sprvisorTel = offer.SprvisorTel
        app.sprvisorFax = offer.SprvisorFax
        app.duree = offer.duree
        app.theme = offer.theme
        app.strtDate = offer.strtDate
        app.endDate = offer.endDate
        app.save()
        return redirect('InternOffers')

    context = {'offers': offers, 'total_offers': total}
    return render(request, 'InternOffers.html', context)

@admin_redirect
@login_required(login_url='Signin')
@allowed_users(allowed_roles=['univStudents'])
def StudentHome(request,):
    context = { }
    return render(request,"StudentHome.html", context)

@login_required(login_url='Signin')
@allowed_users(allowed_roles=['univStudents'])
def StudentProfile(request):
    #Details = user.objects.all
    context = { }
    return render(request,"StudentProfile.html", context)

@allowed_users(allowed_roles=['univStudents'])
@login_required(login_url='Signin')
def studentEditProfile(request):
    student = request.user.student
    if request.method == 'POST':
        form = StudentEditProfile(request.POST, instance=student)
        if form.is_valid():
            student.username = request.user 
            submmitedform = form.save(commit=False)
            password = form.cleaned_data.get('password')  # Get the new password value from the form
            if password:
                # Set the new password for the user
                request.user.set_password(password)
                request.user.save()
            student.save()
            return redirect('StudentProfile')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = StudentEditProfile(instance=student)
    context = {'form': form}
    return render(request, 'StudentEditProfile.html', context)


@login_required(login_url='Signin')
@allowed_users(allowed_roles=['univStudents'])
def MyApplications(request):
    apps = InternshipApp.objects.filter(applicant = request.user)
    total_apps = apps.count()
    marks = Marks.objects.filter(intern= request.user)
    presence = Attendence.objects.filter(intern= request.user)
    return render(request,"MyApplications.html", { 'myapps': apps , 'total_apps': total_apps, 'marks': marks, 'presence':presence})



def LogoutUser(request):
    logout(request)
    context = { }
    return render(request, "Home.html", context)


@login_required(login_url='Signin')
@allowed_users(allowed_roles=['univStudents'])
def VerifyCode(request):
    if request.method == 'POST':
        entered_code = request.POST.get('Code')    
        verification_obj = VerificationCode.objects.get(user=request.user)
        if not (entered_code):
            messages.error(request, 'Please fill in the required field!')
        else:
            try:
                if entered_code.strip() == verification_obj.code.strip():
                    request.user.student.verifiedLogin = True
                    request.user.student.save()
                    return redirect('StudentHome')

                else:
                    messages.error(request, 'Invalid verification code.')

            except VerificationCode.DoesNotExist:
                messages.error(request, 'Invalid verification code,please wait for administration approval')

    context = {}
    return render(request, "VerificationCode.html", context)

@login_required(login_url='Signin')
@allowed_users(allowed_roles=['univStudents'])
def VerificationPage(request):       
    context = {}
    return render(request, "VerificationCode.html", context)

@unauthenticated_user
def Signin(request):
    if request.method == 'POST':
        username = request.POST.get('fullname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.get(username=username)
        try:
            if not (username and email and password):
                messages.error(request, 'Please fill in all the required fields!')
            else:
                user = authenticate(request, username=username, email=email, password=password)
                if hasattr(user, 'student'):
                    if user is not None:
                        login(request, user)
                        if user.student.verifiedLogin is not True:
                            return redirect('VerificationPage')
                        else:
                            return redirect('StudentHome')
                    else:
                        messages.error(request, 'Invalid credentials!')
                else:
                    if user is not None:
                        login(request, user)
                        return redirect('StudentHome') 
                    else:
                        messages.error(request, 'Invalid credentials!')

        except User.DoesNotExist:
            messages.error(request, 'User does not exist.')
            return redirect('Signin')

    context = {}
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
            Supervisor.objects.create(username=user,email=email,password=password)
            #your_model_instance = InternshipApp(internMaster=user)--the right thing to do instead is to write:
            #InternshipApp.objects.create(internMaster=user)
            #your_model_instance.save()--to remove
            messages.success(request, "Account Created successfully")
    context = {'form': form }
    return render(request, "CreateSupervisor.html", context)