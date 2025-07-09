from django.urls import path
from . import views

urlpatterns = [
    path('patientinfo_page/', views.patientinfo_page, name='patientinfo_page'),
    path('patient_login', views.patient_login, name='patient_login'),
    path('changepatient', views.changepatient, name='changepatient'),
    path('patient_enter_otp', views.patient_enter_otp, name='patient_enter_otp'),
    path('change_patient_credentials', views.change_patient_credentials, name='change_patient_credentials'),
    path('lab_report', views.lab_report, name='lab_report'),
    path('book_appointment/<int:id>/',views.book_appointment,name='book_appointment'),
    path('see_appointments',views.see_appointments,name='see_appointments'),
    path('patient_prescription', views.patient_prescription, name='patient_prescription'),
    path('reminder',views.reminder,name='reminder')


    ]
