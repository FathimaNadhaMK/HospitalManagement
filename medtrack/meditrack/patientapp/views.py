from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.shortcuts import render
from adminapp.models import DoctorAvailability
from .models import PatientModel, LabReport, BookAppointment, PrescriptionModel,Reminder

from .models import PatientModel
import random
from django.core.mail import send_mail

from adminapp.views import send_email
from django.contrib import messages
from django.utils import timezone
from .forms import ReminderForm

# Create your views here.
def patient(request):
    return render(request,'patient_page.html')


from django.utils import timezone
from datetime import timedelta, date
from adminapp.models import DoctorAvailability  # adjust if this model is elsewhere

@login_required
def patientinfo_page(request):
    patient_id = request.session.get('user_id')
    try:
        patient = PatientModel.objects.get(id=patient_id)

        today = timezone.now().date()
        week_later = today + timedelta(days=7)

        available_doctors = DoctorAvailability.objects.filter(
            availability='Available',
            date__range=(today, week_later)
        ).select_related('doctor_name').order_by('date')

        return render(request, 'patientinfo_page.html', {
            'patient': patient,
            'available_doctors': available_doctors
        })
    except PatientModel.DoesNotExist:
        return redirect('patient_login')


def patient_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            patient = PatientModel.objects.get(username=username, password=password)
            request.session['user_id'] = patient.id
            return redirect('patientinfo_page')
        except PatientModel.DoesNotExist:
            messages.info(request, "Enter correct Username or Password")
            return redirect('patient_login')

    return render(request, 'patient_login.html')





def changepatient(request):
    if request.method=='POST':
        username = request.POST['username']
        patient_id=request.session.get('user_id')
        pt= PatientModel.objects.get(id=patient_id)
        current_pt =pt.username

        if username==current_pt:
            try:
                patient=PatientModel.objects.get(username=username)
                pt_email = patient.email
                subject='medTrack patient Details'
                otp= random.randint(1000,9999)
                send_email(subject,str(otp),pt_email)
                request.session['pt_otp']=otp
                return redirect('patient_enter_otp')
            except:
                messages.info(request,'User does not Exist')
                return redirect('admin_page')
        else:
            messages.info(request, 'Correct your username')
            return redirect('changepatient')
    return render(request,'username_passwordpt.html')




def patient_enter_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST['otp']
        print(entered_otp)
        session_otp = request.session.get('pt_otp')
        s_otp = str(session_otp)
        print(s_otp)
        if entered_otp == s_otp:
            return redirect('change_patient_credentials')
        else:
            messages.info(request,'Invalid OTP')
            return redirect('patient_enter_otp')
    return render(request,'pt_otppage.html')

def change_patient_credentials(request):
    if request.method == 'POST':
        new_username = request.POST['newUsername']
        new_password = request.POST['newPassword']
        conf_password = request.POST['confirmPassword']

        try:
            pt = PatientModel.objects.get(username=new_username)
            messages.info(request, 'Username already exists.Try another one')
            return redirect('change_patient_credentials')
        except:
            if new_password == conf_password:
                patientid = request.session.get('user_id')
                pt=PatientModel.objects.get(id=patientid)
                pt.username = new_username
                pt.password = new_password
                pt.save()
                return redirect('patientinfo_page')
            else:
                messages.info(request,'Password does not match')

    return render(request, 'change_patient_credentials.html')

def patient_logout(request):
    if 'patient_id' in request.session:
        request.session.flush()
    return redirect('patient_login')

def lab_report(request):
    pt_id = request.session.get('user_id')
    pt_data = PatientModel.objects.get(id=pt_id)
    pt_username = pt_data.username
    if request.method == 'POST':

        print('username',pt_username)
        test=request.POST['test_name']
        report = request.FILES['report_file']
        upload_report = LabReport(name=pt_username,test_name=test,image=report)
        upload_report.save()
        return redirect('patientinfo_page')
    report_data = LabReport.objects.filter(name=pt_username)
    return render(request,'lab_report.html',{"report_data":report_data})



def book_appointment(request,id):
    pt_id=request.session.get('user_id')
    pt_data = PatientModel.objects.get(id=pt_id)
    doc_data=DoctorAvailability.objects.get(id=id)
    #print(doc_data.doctor_name)
    doctor=doc_data.doctor_name
    date=doc_data.date

    total_booking= BookAppointment.objects.filter(doc_name=doctor, date=date)
    last_token =len(total_booking)

    if last_token<100:
        token=last_token+1
        booking = BookAppointment(pt_name=pt_data,doc_name=doctor,date=date,token=token,status=True)
        booking.save()
        return JsonResponse({
            'status':'success',
            'message':f'Appointment booked succesfully! your token number is {token}'
        })

        return redirect('patientinfo_page')

    else:
        booking = BookAppointment(pt_name=pt_data, doc_name=doctor, date=date,token =0)
        booking.save()

        return JsonResponse({
            'status': 'Failed',
            'message': f'Appointment booked Failed!'
        })

        return redirect('patientinfo_page')

    return redirect('update_availability')

from datetime import date
from .models import BookAppointment, PatientModel

def see_appointments(request):
    pt_id = request.session.get('user_id')
    pt = PatientModel.objects.get(id=pt_id)

    all_appts = BookAppointment.objects.filter(pt_name=pt).select_related('doc_name', 'doc_name__department').order_by('-date')

    today = date.today()
    todays_appointments = all_appts.filter(date=today, status=True)
    upcoming_appointments = all_appts.filter(date__gt= today, status=True).order_by('date')
    denied_appointments = all_appts.filter(status=False).order_by('-date')
    past_appointments = all_appts.filter(date__lt=today,status=True)

    return render(request, 'see_appointments.html', {
        'todays_appointments': todays_appointments,
        'upcoming_appointments': upcoming_appointments,
        'past_appointments': past_appointments,
        'denied_appointments':denied_appointments
    })


def patient_prescription(request):
    pt_id = request.session.get('user_id')
    patient = PatientModel.objects.get(id=pt_id)
    pt_username=patient.username
    prescriptions = PrescriptionModel.objects.filter(patient_name=pt_username)


    return render(request, 'patient_prescription.html', {'prescriptions': prescriptions})

def reminder(request):
    form= ReminderForm()
    doc_reminder=Reminder.objects.filter(remind_at_lte=timezone.now())

    if form.is_valid():
        form.save()
        return redirect('patientinfo_page')
    return render(request,'reminder.html',{form:form,doc_reminder:doc_reminder})