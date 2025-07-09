from django.contrib import admin


# Register your models here.

from .models import DepartmentModel,DoctorModel


admin.site.register(DoctorModel)
admin.site.register(DepartmentModel)
