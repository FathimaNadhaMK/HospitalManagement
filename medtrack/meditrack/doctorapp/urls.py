from django.urls import path
from . import views

urlpatterns=[
    path('',views.doctor_login,name='doctor_login'),
    path('doctor_page',views.doctor_page,name='doctor_page'),
    path('doctor_logout',views.doctor_logout,name='doctor_logout'),
    path('patient_profile_for_access',views.patient_profile_for_access,name='patient_profile_for_access'),
    path('add_pres',views.add_prescription,name='add_prescription'),
    path('change',views.change,name='change'),
    path('enter_otp',views.enter_otp,name='enter_otp'),
    path('change-credentials',views.change_credentials,name='change_credentials')
]