from django.contrib.auth.models import AbstractUser
from django.db import models

from recipes.managers import CustomUserManager
from recipes.validators import validate_pos_value
from recipes.auth import  *


class MedicineType(models.Model):
    type_name = models.CharField(max_length=50)

    def __str__(self):
        return self.type_name


class City(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    

class User(AbstractUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=12, unique=True)
    is_admin = models.BooleanField(default=False)

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
   
   
class Hospital(models.Model):
    city = models.ForeignKey(City, null=False, on_delete=models.CASCADE)
    hospital_name = models.CharField(max_length=20)
    
    def __str__(self):
        return self.hospital_name


class Doctor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, null=True, on_delete=models.CASCADE)

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
    medicine_card_number = models.CharField(max_length=10, null=True, blank=True)
    medicine_policy_number = models.CharField(max_length=16, null=True, blank=True)
    comment = models.TextField(blank=True, null=True)
    
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
        return MedicineRequest.objects.filter(recipe=self)
    

class Pharmacy(models.Model):
    pharmacy_name = models.CharField(max_length=20)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True)
    pharmacy_address = models.TextField()
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.pharmacy_name


class Apothecary(models.Model):
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE)
    user = models.ForeignKey(User, unique=True, on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {}'.format(self.user.email, self.pharmacy.pharmacy_name)


class MedicineRequestStatus(models.Model):
    status_name = models.CharField(max_length=20)


class MedicineName(models.Model):
    medicine_name = models.CharField(max_length=50, unique=True)
    medicine_level = models.PositiveSmallIntegerField(default=0)
    
    @property
    def medicine_types(self):
        return MedicineType.objects.filter(medicine__medicine_name_id=self.id)
    
    def __str__(self):
        return self.medicine_name


class Medicine(models.Model):
    medicine_name = models.ForeignKey(MedicineName, on_delete=models.CASCADE)
    medicine_type = models.ForeignKey(MedicineType, on_delete=models.CASCADE)
    pharmacies = models.ManyToManyField(Pharmacy, through='MedicinesPharmacies')

    def __str__(self):
        return '{} {}'.format(self.medicine_name.medicine_name, self.medicine_type.type_name)
    
    @property
    def name(self):
        return self.medicine_name.medicine_name
    
    @property
    def type(self):
        return self.medicine_type.type_name


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

    @property
    def medicine_name_id(self):
        return self.medicine_dosage.medicine.id
    

class MedicinesPharmacies(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0, validators=[validate_pos_value])
    price = models.FloatField(default=0.0, validators=[validate_pos_value])
    
    @property
    def name(self):
        return self.medicine.name
    
    @property
    def type(self):
        return self.medicine.type
        
    @property
    def level(self):
        return self.medicine.medicine_name.medicine_level

