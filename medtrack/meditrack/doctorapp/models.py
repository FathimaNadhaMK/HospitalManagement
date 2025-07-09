from django.db import models

# Create your models here.
class DepartmentModel(models.Model):
    name= models.CharField(max_length=100)

    def __str__(self):
        return self.name


class DoctorModel(models.Model):
    GENDER_CHOICES =[
        ('Male','Male'),
        ('Female','Female'),
        ('Other','Other')
    ]
    image=models.ImageField(upload_to='doctor_img')
    username = models.CharField(max_length=100)
    firstname=models.CharField(max_length=100)
    lastname=models.CharField(max_length=100)
    profile_summary=models.TextField()
    email = models.EmailField()
    gender = models.CharField(
        choices=GENDER_CHOICES,
        max_length=20,
        default='Female'
    )
    phone_no = models.CharField(max_length=11)
    qualification = models.CharField(max_length=100)
    department = models.ForeignKey(DepartmentModel,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    password= models.CharField(max_length=100)

    def __str__(self):
      return self.firstname


