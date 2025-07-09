from django.db import models

# Create your models here.
from django.db  import models
from doctorapp.models import DoctorModel

# Create your models here.
class DoctorAvailability(models.Model):
    choice_available = [
        ('Available', 'Available'),
        ('Not Available', 'Not Available'),
    ]
    doctor_name = models.ForeignKey(DoctorModel, on_delete=models.CASCADE)
    date = models.DateField()
    available_time=models.CharField(max_length=100,default='09.00 am - 01.00pm')
    availability = models.CharField(max_length=20,
                                    choices=choice_available,
                                    default='Available')

# Create your models here.