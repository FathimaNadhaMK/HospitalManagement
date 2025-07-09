

from django.db import models
from doctorapp.models import DoctorModel
from django.utils import timezone


# Create your models here.
class PrescriptionModel(models.Model):
    doctor_name=models.CharField(max_length=100)
    patient_name=models.CharField(max_length=100,default="name")
    date=models.DateField(auto_now_add=True)
    prescription=models.TextField()


    def __str__(self):
      return self.doctor_name

class PatientModel(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    ]

    username = models.CharField(max_length=100)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    age=models.IntegerField()
    dob=models.DateField()

    email = models.EmailField()
    gender = models.CharField(
        choices=GENDER_CHOICES,
        max_length=20,
        default='Female'
    )
    phone_no = models.CharField(max_length=11)
    bystandphone_no=models.CharField(max_length=11)
    place=models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    password = models.CharField(max_length=100)



    def __str__(self):
      return self.firstname

class LabReport(models.Model):
    name=models.CharField(max_length=100)
    added_date=models.DateField(auto_now_add=True)
    test_name=models.CharField(max_length=100)
    image=models.FileField(upload_to='lab_report')

    def __str__(self):
        return self.name

class BookAppointment(models.Model):
    pt_name = models.ForeignKey(PatientModel,on_delete=models.CASCADE)
    doc_name=models.ForeignKey(DoctorModel,on_delete=models.CASCADE)
    date = models.DateField()
    token=models.IntegerField(blank=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.pt_name} - {self.token}'

class Reminder(models.Model):
    pt_name=models.ForeignKey(PatientModel,on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
    description=models.TextField(blank=True)
    remind_at=models.DateTimeField()
    created_at=models.DateTimeField(auto_now_add=True)

    def is_due(self):
        return timezone.now() >= self.remind_at

    def __str__(self):
        return f'{self.title} - {self.pt_name}'



