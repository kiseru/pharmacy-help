from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField

from recipes.models import Recipe, MedicineRequest, User, Medicine, MedicineType, MedicineName, Pharmacy, \
  MedicinesPharmacies
from rest_framework import serializers
import re

# class JsonSerializer:
#     @staticmethod
#     def get_json(object):
#         return object.__str__()


def serialize_user(user, errors: list):
    result = UserSerializer(instance=user)
    result.data['error'] = None if not errors else ''.join([''.join([j[1][0]['message'] for j in i.items()]) for i in errors])
    return result.data


class RecipeShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'doctorName', 'patientName', 'patient_email', 'date')
    id = CharField(source='token')
    doctorName = CharField(source='get_doctor_initials')
    patientName = CharField(source='patient_initials')
    date = CharField(source='get_date_str')
    

class MedicineRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicineRequest
        fields = ['id', 'medicine_name_id', 'is_accepted', 'medicine_name', 'medicine_frequency', 'medicine_dosage', 'medicine_period']


class RecipeFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'doctor_initials', 'doctor_email', 'patient_initials', 'patient_email',
                  'date', 'day_duration', 'patient_age', 'medicine_card_number', 'medicine_policy_number', 'requests')
    id = CharField(source='token', required=False)
    doctor_initials = CharField(source='get_doctor_initials', required=False)
    doctor_email = CharField(source='get_doctor_email', required=False)
    date = CharField(source='get_date_str', required=False)
    requests = MedicineRequestSerializer(many=True, required=False)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'last_name', 'first_name', 'phone_number', 'role', 'is_admin', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }
        
    def is_valid(self, raise_exception=False):
        if super().is_valid(raise_exception=raise_exception):
            if len(self.initial_data['password']) < 5:
                self._errors['password'] = 'Password can not be less than 5 symbols'
                if raise_exception:
                    raise ValidationError()
            else:
                self.validated_data['password'] = self.initial_data['password']
            if not re.fullmatch('([^\W\d_]| )+', self.initial_data['first_name']):
                self._errors['first_name'] = 'First name should contain only letters or "-"'
                if raise_exception:
                    raise ValidationError()
            if not re.fullmatch('([^\W\d_]| )+', self.initial_data['last_name']):
                self._errors['first_name'] = 'Last name should contain only letters or "-"'
                if raise_exception:
                    raise ValidationError()
        return not len(self.errors)
        

class MedicineTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicineType
        fields = ('id', 'type_name')


class MedicineNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicineName
        fields = ('id', 'medicine_name', 'medicine_types')
    medicine_types = MedicineTypeSerializer(many=True)
    
    
class PharmacySerializer(serializers.ModelSerializer):
    class Meta:
        model = Pharmacy
        fields = '__all__'
        
        
class MedicineWithPharmaciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = ('medicine_name', 'medicine_type', 'pharmacies')
    medicine_name = CharField(source='name')
    medicine_type = CharField(source='type')
    pharmacies = PharmacySerializer(many=True)
    
    
# class MedicinePharmacySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = MedicinesPharmacies
#         exclude = ('count',)
#     medicine = MedicineSerializer()
#     pharmacy = PharmacySerializer()


class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = ('medicine_name', 'medicine_type')
    medicine_name = CharField(source='name')
    medicine_type = CharField(source='type')


class GoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicinesPharmacies
        fields = ('count', 'price', 'name', 'type', 'description', 'id')
