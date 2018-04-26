from django.contrib.auth.models import AbstractUser
from django.db import models

from recipes.managers import CustomUserManager
from recipes.auth import  *

class MedicineType(models.Model):
    type_name = models.CharField(max_length=50)

    def __str__(self):
        return self.type_name


class User(AbstractUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=12, unique=True)

    username = None

    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number', 'password']
    USERNAME_FIELD = 'email'

    # def save(self, *args, **kwargs):
    #     self.set_password(self.password)
    #     super().save(*args, **kwargs)

    objects = CustomUserManager()

    def __str__(self):
        return '{0} {1}'.format(self.first_name, self.last_name)
    
    @property
    def role(self):
        return get_role(self)
    

class Doctor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email
    
    def get_initials(self):
        return str(self.user)


class Recipe(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient_email = models.CharField(max_length=50)
    patient_initials = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now=True)
    token = models.TextField()
    day_duration = models.PositiveIntegerField(default=15)
    patient_age = models.PositiveSmallIntegerField()
    medicine_card_number = models.CharField(max_length=10, null=True)
    medicine_policy_number = models.CharField(max_length=16, null=True)
    
    def get_date_str(self):
        return self.date.strftime('%d.%m.%Y')
    
    def __str__(self):
        return '{} - {} - {}'.format(self.date, self.patient_email, self.doctor.user.email)
    
    def get_doctor_initials(self):
        return self.doctor.get_initials()
    
    def get_doctor_email(self):
        return self.doctor.user.email
    
    @property
    def requests(self):
        return self.medicinerequest_set.all()
    

class Pharmacy(models.Model):
    pharmacy_name = models.CharField(max_length=20)
    pharmacy_address = models.TextField()

    def __str__(self):
        return self.pharmacy_name


class Apothecary(models.Model):
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {}'.format(self.user.email, self.pharmacy.pharmacy_name)


class MedicineRequestStatus(models.Model):
    status_name = models.CharField(max_length=20)


class MedicineName(models.Model):
    medicine_name = models.CharField(max_length=50)
    medicine_description = models.TextField()
    medicine_level = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.medicine_name


class Medicine(models.Model):
    medicine_name = models.ForeignKey(MedicineName, on_delete=models.CASCADE)
    medicine_type = models.ForeignKey(MedicineType, on_delete=models.CASCADE)
    pharmacies = models.ManyToManyField(Pharmacy, through='recipes.MedicinesPharmacies')

    def __str__(self):
        return '{} {}'.format(self.medicine_name.medicine_name, self.medicine_type.type_name)


class MedicineDosage(models.Model):
    dosage = models.TextField()
    frequency = models.TextField()
    period = models.TextField()
    medicine = models.ForeignKey(MedicineName, on_delete=models.CASCADE)

    def __str__(self):
        return '{} {} {}'.format(self.medicine.medicine_name.medicine_name, self.dosage, self.frequency)


class MedicineRequest(models.Model):
    # medicine_request_status = models.ForeignKey(MedicineRequestStatus, on_delete=models.CASCADE)
    medicine_dosage = models.ForeignKey(MedicineDosage, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    medicine_count = models.SmallIntegerField(default=0)
    given_medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, null=True, blank=True)
    request_confirmation_time = models.DateTimeField(null=True, blank=True)
    apothecary = models.ForeignKey(Apothecary, on_delete=models.CASCADE, null=True, blank=True)
    
    @property
    def is_accepted(self):
        return self.medicine_count > 0

    @property
    def medicine_frequency(self):
        return self.medicine_dosage.frequency
    
    @property
    def dosage(self):
        return self.medicine_dosage.dosage
    
    @property
    def medicine_period(self):
        return self.medicine_dosage.period
    
    @property
    def medicine_name(self):
        return self.medicine_dosage.medicine.medicine_name
    

class MedicinesPharmacies(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE)
    count = models.PositiveIntegerField()
    price = models.FloatField()
