from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import PharmacistModel, MedicineAvailability,AllottedOrNotMedcine

# Register your models here.
admin.site.register(PharmacistModel)

class MedicineAdmin(admin.ModelAdmin):
    list_display = ['name','price','available','created_at','updated_at','quantity','description']
    list_editable = ['price','quantity','available']
    prepopulated_fields = {'medicine_code':('name',)}
    list_per_page = 7

admin.site.register(MedicineAvailability,MedicineAdmin)
admin.site.register(AllottedOrNotMedcine)
