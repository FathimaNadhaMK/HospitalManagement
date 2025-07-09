from django import forms
from doctorapp.models import DoctorModel,DepartmentModel
from patientapp.models import PatientModel
from pharmacistapp.models import PharmacistModel

class DoctorUpdateForm(forms.ModelForm):
    class Meta:
        model= DoctorModel
        fields = '__all__'

class PatientUpdateForm(forms.ModelForm):
    class Meta:
        model= PatientModel
        fields = '__all__'

class PharmacistUpdateForm(forms.ModelForm):
    class Meta:
        model=  PharmacistModel
        fields = '__all__'



class DepartmentForm(forms.ModelForm):
    class Meta:
         model = DepartmentModel
         fields = '__all__'

