import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from doctorapp.models import DoctorModel,DepartmentModel

from patientapp.models import PatientModel,PrescriptionModel
from pharmacistapp.models import PharmacistModel
from .forms import DoctorUpdateForm,PharmacistUpdateForm,PatientUpdateForm,DepartmentForm
from .models import DoctorAvailability



#ftgx svkh gonu lape

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = "fathimanadhamk@gmail.com"
EMAIL_PASSWORD = "ftgx svkh gonu lape"

def send_email(sub,mssg,EMAIL_RECEIVER):
    try:
        msg= MIMEMultipart()
        msg['from']=EMAIL_SENDER
        msg['to']=EMAIL_RECEIVER
        msg['subject']=sub
        body=mssg
        msg.attach(MIMEText(body,'plain'))

        server = smtplib.SMTP(SMTP_SERVER,SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER,EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER,EMAIL_RECEIVER,msg.as_string())
        server.quit()

        print("Email sent successfully")
    except Exception as e:
        print(f"error: {e}")


# Create your views here.
def index(request):
    return render(request, 'index.html')


def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        admin = auth.authenticate(username=username, password=password)
        if admin is not None:
            auth.login(request, admin)
            return redirect('admin_page')
        else:
            messages.info(request, 'invalid username or password')
            return redirect('admin_login')

    return render(request, 'admin_login.html')


@login_required
def admin_page(request):
    doctor_data=DoctorModel.objects.all()
    patient_data= PatientModel.objects.all()
    pharmacist_data=PharmacistModel.objects.all()
    department_data=DepartmentModel.objects.all()
    return render(request, 'admin_page.html',{"doctors_data":doctor_data,"patient_data":patient_data,"pharmacist_data":pharmacist_data,"department_data":department_data})



def logout(request):
    auth.logout(request)
    return redirect('/')


@login_required()
def doctor_create(request):
    if request.method == 'POST':
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        profile_summary = request.POST.get('profile_summary', '')
        gender = request.POST.get('gender', '')
        department = request.POST['department']  # This should be an ID (string)
        phone_no = request.POST['phone_no']
        qualification = request.POST['qualification']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        image = request.FILES['image']

        if password == confirm_password:
            if DoctorModel.objects.filter(username=username).exists():
                messages.info(request, "User already exists")
                return redirect('doctor_create')

            elif DoctorModel.objects.filter(email=email).exists():
                messages.info(request, "Email already registered")
                return redirect('doctor_create')

            elif DoctorModel.objects.filter(phone_no=phone_no).exists():
                messages.info(request, "Phone number already used")
                return redirect('doctor_create')

            else:

                dept = DepartmentModel.objects.get(id=department)
                doctor_data = DoctorModel(
                    username=username,
                    firstname=firstname,
                    lastname=lastname,
                    profile_summary=profile_summary,
                    gender=gender,
                    email=email,
                    phone_no=phone_no,
                    department=dept,
                    qualification=qualification,
                    password=password,
                    image=image
                )
                doctor_data.save()

                subject = "Medi-Track Doctor Details"
                message = f'Username: {username}\nPassword: {password}'
                send_email(subject, message, email)

                return redirect('admin_page')
        else:
            messages.info(request, "Passwords do not match")
            return redirect('doctor_create')

    return render(request, 'doctor_create.html')


def patient_page(request):

    if request.method == 'POST':
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        gender = request.POST.get('gender', '')
        phone_no = request.POST['phone_no']
        bystandphone_no = request.POST['bystandphone_no']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        dob=request.POST['dob']
        place=request.POST['place']
        age=request.POST['age']

        if password == confirm_password:

          if PatientModel.objects.filter(username=username).exists():
             messages.info(request, "User Already Exists")
             return redirect('patient_page')

          elif PatientModel.objects.filter(email=email).exists():

              messages.info(request, "User Already Exists")
              return redirect('patient_page')

          else:

             patient_data = PatientModel(username=username,
                                      firstname=firstname,
                                      lastname=lastname,
                                      age=age,
                                      gender=gender,
                                      email=email,
                                      phone_no=phone_no,
                                      bystandphone_no=phone_no,
                                      dob=dob,
                                      place=place,
                                      password=password,
                                      )
          patient_data.save()
          subject = " Medi-Track Patient Details"
          message = (f'username = {username}\n'
                     f'password = {password}')
          send_email(subject, message, email)
          return redirect('admin_page')

        else:
         messages.info(request, "password is not matching")
         return redirect('patient_page')



    return render(request, 'patient_page.html')


def pharmacist_create(request):
    if request.method == 'POST':
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        gender = request.POST.get('gender', '')
        email = request.POST['email']
        phone_no = request.POST['phone_no']
        qualification = request.POST['qualification']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        profile_summary=request.POST['profile_summary']




        if password == confirm_password:
            if PharmacistModel.objects.filter(username=username).exists():
                messages.info(request, "Username already exists")
                return redirect('pharmacist_create')
            elif PharmacistModel.objects.filter(email=email).exists():
                messages.info(request, "Email already registered")
                return redirect('pharmacist_create')
            elif PharmacistModel.objects.filter(phone_no=phone_no).exists():
                messages.info(request, "Phone number already registered")
                return redirect('pharmacist_create')



            pharmacist_data = PharmacistModel(
                username=username,
                first_name=firstname,
                last_name=lastname,
                gender=gender,
                profile_summary=profile_summary,
                email=email,
                phone_no=phone_no,
                qualification=qualification,
                password=password,


            )
            pharmacist_data.save()

            subject = "Medi-Track Pharmacist Details"
            message = f'Username: {username}\nPassword: {password}'
            send_email(subject, message, email)

            return redirect('admin_page')
        else:
            messages.info(request, "Passwords do not match")
            return redirect('pharmacist_create')

    return render(request, 'pharmacist_create.html')







@login_required
def doctor_delete(request,id):
    doctor = DoctorModel.objects.get(id=id)
    doctor.delete()
    return redirect('admin_page')



@login_required
def patient_delete(request,id):
    patient = PatientModel.objects.get(id=id)
    patient.delete()
    return redirect('admin_page')

@login_required
def pharma_delete(request,id):
    pharmacist = PharmacistModel.objects.get(id=id)
    pharmacist.delete()
    return redirect('admin_page')

@login_required
def doc_update(request,id):
    doctor=DoctorModel.objects.get(id=id)
    doc_update=DoctorUpdateForm(request.POST or None,request.FILES or None,instance=doctor)
    if doc_update.is_valid():
        doc_update.save()
        return redirect('admin_page')
    return render(request,'doctor_update.html',{"doc_update":doc_update,"doctor":doctor})


#
@login_required
def patient_update(request,id):
    patient=PatientModel.objects.get(id=id)
    patient_update=PatientUpdateForm(request.POST or None,request.FILES or None,instance=patient)
    if patient_update.is_valid():
        patient_update.save()
        return redirect('admin_page')
    return render(request,'patient_update.html',{"patient_update":patient_update,"patient":patient})



@login_required
def pharm_update(request,id):
    pharmacist=PharmacistModel.objects.get(id=id)
    pharm_update=PharmacistUpdateForm(request.POST or None,request.FILES or None,instance=pharmacist)
    if pharm_update.is_valid():
        pharm_update.save()
        return redirect('admin_page')
    return render(request,'pharm_update.html',{"pharm_update":pharm_update,"pharmacist":pharmacist})



def doctor_login(request):
    return render(request,'doctor_login.html')


def pharmacist_login(request):
    return render(request,'pharmacist_login.html')

def patient_login(request):
    return render(request,'patient_login.html')


def create_department(request):
    dept_data= DepartmentModel.objects.all()
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('create_department')
    else:
        form=DepartmentForm()

    return render(request, 'create_department.html',{'form':form,'dept_data':dept_data})


@login_required
def delete_department(request,id):
    department_dt = DepartmentModel.objects.get(id=id)
    department_dt.delete()
    return redirect('admin_page')

@login_required
def update_availability(request,id):
    doctor=DoctorModel.objects.get(id=id)
    doctor_name=doctor.firstname
    if request.method=='POST':
        date=request.POST['date']
        availability=request.POST['availability']
        try:
           check_avail=DoctorAvailability.objects.get(doctor_name=doctor,date=date)
           check_avail.availability=availability
           check_avail.date=date
           check_avail.save()
           return redirect('admin_page')
        except:
            try:
                 doc_availability=DoctorAvailability(doctor_name=doctor,
                                            date=date,
                                            availability=availability)
                 doc_availability.save()
                 return redirect('admin_page')
            except:
                 messages.info(request,"something went wrong")
    return render(request,'update_availability.html')


