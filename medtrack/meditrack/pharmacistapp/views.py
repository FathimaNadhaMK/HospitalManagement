from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

from django.shortcuts import render, redirect
from django.template.context_processors import request

from adminapp.views import send_email
from django.contrib import messages
from django.template.defaultfilters import length

from .models import PharmacistModel,MedicineAvailability,AllottedOrNotMedcine
from patientapp.models import PatientModel,PrescriptionModel

import random
# Create your views here.
import datetime

def pharmacist_page(request):
    ph_id = request.session.get("user_id")

    pharmacist_dt = PharmacistModel.objects.get(id=ph_id)
    if request.method == 'POST':
        pt_username = request.POST['search']
        request.session['pt_username']=pt_username
        try:
            patient_data = PatientModel.objects.get(username=pt_username)

            request.session['pt_id'] = patient_data.id
            return redirect('pharmacist_access_patient')
        except PatientModel.DoesNotExist:
            messages.info(request, "Enter correct Username")
            return redirect('pharmacist_page')

    return render(request, 'pharmacist_page.html', {"pharmacist_dt": pharmacist_dt})


def  pharmacist_access_patient(request):
    pt_id = request.session.get('pt_id')
    patient_dt = PatientModel.objects.get(id=pt_id)
    pt_username = patient_dt.username

    prescription = PrescriptionModel.objects.filter(patient_name=pt_username)
    length_p=len(prescription)
    prescriptions=prescription[length_p-1]


    # If the request is made by a doctor, show the form
    pharmacist_id = request.session.get('user_id')



    return render(
        request,
        'pharmacist_access_patient.html',
        {
            "patient_dt": patient_dt,
            "prescription": prescriptions,

        }
    )



def pharmacist_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            pharmacist=PharmacistModel.objects.get(username=username ,password=password)
            request.session['user_id']=pharmacist.id
            return redirect('pharmacist_page')
        except:
            messages.info(request,"Enter correct Username or Password")
            return redirect('pharmacist_login')
    return render(request,'pharmacist_login.html')


def changeph(request):
    if request.method=='POST':
        username = request.POST['username']
        pharmacistid=request.session.get('user_id')
        ph= PharmacistModel.objects.get(id=pharmacistid)
        current_ph =ph.username

        if username==current_ph:
            try:
                pharmacist=PharmacistModel.objects.get(username=username)
                ph_email = pharmacist.email
                subject='medTrack patient Details'
                otp= random.randint(1000,9999)
                send_email(subject,str(otp),ph_email)
                request.session['ph_otp']=otp
                return redirect('enter_otp')
            except:
                messages.info(request,'User does not Exist')
                return redirect('admin_page')
        else:
            messages.info(request, 'Correct your username')
            return redirect('changeph')
    return render(request,'username_password.html')

def enter_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST['otp']
        print(entered_otp)
        session_otp = request.session.get('ph_otp')
        s_otp = str(session_otp)
        print(s_otp)
        if entered_otp == s_otp:
            return redirect('change_credentialss')
        else:
            messages.info(request,'Invalid OTP')
            return redirect('enter_otp')
    return render(request,'ph_otppage.html')

def change_credentialss(request):
    if request.method == 'POST':
        new_username = request.POST['newUsername']
        new_password = request.POST['newPassword']
        conf_password = request.POST['confirmPassword']

        try:
            ph = PharmacistModel.objects.get(username=new_username)
            messages.info(request, 'Username already exists.Try another one')
            return redirect('change_credentialss')
        except:
            if new_password == conf_password:
                pharmacist_id = request.session.get('user_id')
                ph = PharmacistModel.objects.get(id=pharmacist_id)
                ph.username = new_username
                ph.password = new_password
                ph.save()
                return redirect('pharmacist_page')
            else:
                messages.info(request,'Password does not match')

    return render(request, 'change_credentialss.html')



def pharmacist_logout(request):
    if 'pharmacist_id' in request.session:
        request.session.flush()
    return redirect('pharmacist_login')
# Create your views here.
def patient(request):
    return render(request,'pharmacist_create.html')


def medicine_search(request):
    if request.method == 'POST':
        medicine_name = request.POST['search']  # input name must be 'search'
        try:
            medicine = MedicineAvailability.objects.get(name=medicine_name)
            request.session['medicine_name']=medicine_name
            return render(request, 'medicine_search.html', {'medicines': [medicine]})  # wrap in list for loop
        except MedicineAvailability.DoesNotExist:
            messages.info(request, "Medicine not found.")
            return redirect('pharmacist_page')
    else:
        return redirect('pharmacist_page')

def edit_stock(request):
    medicine_name=request.session.get('medicine_name')
    med=MedicineAvailability.objects.get(name=medicine_name)
    qty=None
    if request.method == 'POST':
        qty=request.POST['qty']
        qty=int(qty)
        med.less_qty(qty)
        med.change_availability()
        return  redirect('pharmacist_page')
    return redirect('pharmacist_page')



def alloted_med(request):
    current_date=datetime.date.today()
    pt_username=request.session.get('pt_username')
    print('date',current_date)
    print('name',pt_username)

    if request.method=='POST':
        med_name=request.POST['medicine_name']
        print('medicine:',med_name)
        try:
            alloted_data=AllottedOrNotMedcine.objects.get(date=current_date,name=pt_username)
            med_data=MedicineAvailability.objects.get(name=med_name)
            if med_data.available == True:
                alloted_data.allotted_medicines.add(med_data)
            else:
                alloted_data.not_alloted_medicines.add(med_data)
            return redirect('add_medicines')
        except:
            alloted_datas=AllottedOrNotMedcine(name=pt_username)
            alloted_datas.save()

            alloted_data=AllottedOrNotMedcine.objects.get(date=current_date,name=pt_username)
            med_data = MedicineAvailability.objects.get(name=med_name)

            if med_data.available == True:
                 alloted_data.allotted_medicines.add(med_data)
            else:
                alloted_data.not_allotted_medicines.add(med_data)

            return redirect('add_medicines')

    return render(request,'add_medicines.html')
