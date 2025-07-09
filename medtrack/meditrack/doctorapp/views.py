from django.shortcuts import render, redirect
from django.template.context_processors import request

from .models import DoctorModel,DepartmentModel

from django.contrib import messages

from patientapp.models import PatientModel,PrescriptionModel,LabReport,BookAppointment
from adminapp.views import send_email
import random
from django.utils import timezone




# Create your views here.


def doctor_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            doctors=DoctorModel.objects.get(username=username ,password=password)
            #print(doctor.id,'hyyy')
            request.session['user_id']=doctors.id
            return redirect('doctor_page')
        except:
            messages.info(request,"Enter correct Username or Password")
            return redirect('doctor_login')
    return render(request,'doctor_login.html')

def doctor_page(request):
    d_id = request.session.get("user_id")

    doctor_dt = DoctorModel.objects.get(id=d_id)
    today = timezone.now().date()
    appointments = BookAppointment.objects.filter(
        doc_name=doctor_dt,
        date=today
    ).order_by('token')

    if request.method == 'POST':
        pt_username = request.POST['search']
        try:
            patient_data = PatientModel.objects.get(username=pt_username)
            request.session['pt_id'] = patient_data.id
            return redirect('patient_profile_for_access')
        except PatientModel.DoesNotExist:
            messages.info(request, "Enter correct Username")
            return redirect('doctor_page')

    return render(request, 'doctor_page.html', {"doctor_dt": doctor_dt,"appointments":appointments})



def patient_profile_for_access(request):
    pt_id = request.session.get('pt_id')
    patient_dt = PatientModel.objects.get(id=pt_id)
    pt_username = patient_dt.username

    # Get all prescriptions for the patient
    prescription = PrescriptionModel.objects.filter(patient_name=pt_username)

    # Get all lab reports for the patient
    lab_reports = LabReport.objects.filter(name=pt_username)
    print(lab_reports)

    return render(
        request,
        'patient_profile_for_access.html',
        {
            "patient_dt": patient_dt,
            "prescription": prescription,
            "lab_reports": lab_reports,
        }
    )


def add_prescription(request):
        # doctor
        doctors_id = request.session.get('user_id')
        doctor_dt = DoctorModel.objects.get(id=doctors_id)
        doctor_name = doctor_dt.firstname
        doc_last=doctor_dt.lastname
        doc_fullname=f'{doctor_name} {doc_last}'

        # patient
        pt_id = request.session.get('pt_id')
        patient_dt = PatientModel.objects.get(id=pt_id)

        pt_username = patient_dt.username
        prescription = request.POST['prescription']


        prescription_dt=PrescriptionModel(doctor_name=doc_fullname,
                                          patient_name=pt_username,
                                          prescription=prescription)
        prescription_dt.save()



        return redirect('patient_profile_for_access')

def doctor_logout(request):
    if 'doctors_id' in request.session:
        request.session.flush()
    return redirect('doctor_login')

def change(request):
    if request.method=='POST':
        username = request.POST['username']
        doctor_id=request.session.get('user_id')
        dr= DoctorModel.objects.get(id=doctor_id)
        current_dr =dr.username

        if username==current_dr:
            try:
                doctor=DoctorModel.objects.get(username=username)
                dr_email = doctor.email
                subject='medTrack patient Details'
                otp= random.randint(1000,9999)
                send_email(subject,str(otp),dr_email)
                request.session['dr_otp']=otp
                return redirect('enter_otp')
            except:
                messages.info(request,'User does not Exist')
                return redirect('admin_page')
        else:
            messages.info(request, 'Correct your username')
            return redirect('change')
    return render(request,'username_password.html')

def enter_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST['otp']
        print(entered_otp)
        session_otp = request.session.get('dr_otp')
        s_otp = str(session_otp)
        print(s_otp)
        if entered_otp == s_otp:
            return redirect('change_credentials')
        else:
            messages.info(request,'Invalid OTP')
            return redirect('enter_otp')
    return render(request,'dr_otppage.html')

def change_credentials(request):
    if request.method == 'POST':
        new_username = request.POST['newUsername']
        new_password = request.POST['newPassword']
        conf_password = request.POST['confirmPassword']

        try:
            dr = DoctorModel.objects.get(username=new_username)
            messages.info(request, 'Username already exists.Try another one')
            return redirect('change_credentials')
        except:
            if new_password == conf_password:
                doctorid = request.session.get('user_id')
                dr = DoctorModel.objects.get(id=doctorid)
                dr.username = new_username
                dr.password = new_password
                dr.save()
                return redirect('doctor_page')
            else:
                messages.info(request,'Password does not match')

    return render(request, 'change_credentials.html')

def doctor_logout(request):
    if 'doctor_id' in request.session:
        request.session.flush()
    return redirect('doctor_login')



