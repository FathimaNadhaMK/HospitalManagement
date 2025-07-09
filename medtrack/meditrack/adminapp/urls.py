from django.urls import path
from .import views

urlpatterns=[
 path('',views.index,name='index'),
path('patient_page',views.patient_page,name='patient_page'),
 path('admin_login',views.admin_login,name='admin_login'),
 path('admin_page',views.admin_page,name='admin_page'),
 path('logout',views.logout,name='admin_logout'),
 path('doctor_create',views.doctor_create,name='doctor_create'),
 path('pharmacist_create',views.pharmacist_create,name='pharmacist_create'),
 path('doctor_delete/<int:id>/',views.doctor_delete,name='doctor_delete'),
 path('doc_update/<int:id>/',views.doc_update,name='doc_update'),
 path('patient_delete/<int:id>/',views.patient_delete,name='patient_delete'),
 path('patient_update/<int:id>/',views.patient_update,name='patient_update'),
 path('pharma_delete/<int:id>/',views.pharma_delete,name='pharma_delete'),
 path('pharm_update/<int:id>/',views.pharm_update,name='pharm_update'),
 path('delete_department/<int:id>/',views.delete_department,name='delete_department'),
 path('create_department',views.create_department,name='create_department'),
 path('update_availability/<int:id>/',views.update_availability,name='update_availability')

 ]