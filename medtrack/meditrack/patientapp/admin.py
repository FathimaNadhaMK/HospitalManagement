
from django.contrib import admin
from .models import PatientModel, LabReport, BookAppointment, Reminder
from .models import PrescriptionModel
# Register your models here.
admin.site.register(PatientModel)
admin.site.register(PrescriptionModel)
admin.site.register(LabReport)
admin.site.register(BookAppointment)
admin.site.register(Reminder)

