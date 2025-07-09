from django.db import models

class PharmacistModel(models.Model):
    username = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    profile_summary = models.CharField(max_length=100)
    gender = models.CharField(max_length=20)
    email = models.EmailField()
    phone_no = models.CharField(max_length=15)
    qualification = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    department = models.CharField(max_length=100, default="Pharmacy")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name

class MedicineAvailability(models.Model):
    name = models.CharField(max_length=100,unique=True)
    medicine_code=models.CharField(max_length=20)
    quantity = models.PositiveIntegerField()
    updated_at=models.DateTimeField(auto_now_add=True)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    description=models.CharField(max_length=100)

    def change_availability(self):
        if self.quantity <= 0:
            self.available = False
            self.save()
            return True
        return False

    def less_qty(self,qty):
        if self.quantity >= 1 and qty <= self.quantity:
            self.quantity -= qty
            self.save()
            return True
        return False

    def __str__(self):
            return self.name

class AllottedOrNotMedcine(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField(auto_now=True)
    allotted_medicines = models.ManyToManyField(MedicineAvailability, related_name='allotted_to', blank=True)
    not_allotted_medicines = models.ManyToManyField(MedicineAvailability, related_name='not_allotted_to', blank=True)
