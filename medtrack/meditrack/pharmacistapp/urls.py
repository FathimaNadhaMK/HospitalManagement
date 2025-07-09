from django.urls import path
from . import views


urlpatterns=[
    path('pharmacist_login/', views.pharmacist_login, name='pharmacist_login'),
    path('pharmacist_page', views.pharmacist_page, name='pharmacist_page'),
    path('pharmacist_logout', views.pharmacist_logout, name='pharmacist_logout'),
    path('changeph', views.changeph, name='changeph'),
    path('enter_otp', views.enter_otp, name='enter_otp'),
    path('change-credentialss', views.change_credentialss, name='change_credentialss'),
    path('pharmacist_access_patient', views.pharmacist_access_patient, name='pharmacist_access_patient'),
    path('medicine_search',views.medicine_search,name='medicine_search'),
    path('edit_stock',views.edit_stock,name='edit_stock'),
    path('add-medicines', views.alloted_med, name='add_medicines'),


]
