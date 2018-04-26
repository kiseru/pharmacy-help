from django.contrib.auth.hashers import make_password
from rest_framework.fields import CharField

from recipes.auth import *
from recipes.models import Recipe, MedicineRequest, User
from rest_framework import routers, serializers, viewsets


class JsonSerializer:
    @staticmethod
    def get_json(object):
        return object.__str__()


def serialize_user(user, errors: list):
    result = UserSerializer(instance=user)
    result.data['error'] = None if not errors else ''.join([''.join([j[1][0]['message'] for j in i.items()]) for i in errors])
    return result.data


# class RecipeSerializerShort(JsonSerializer):
#     @staticmethod
#     def get_json(object: Recipe):
#         recipe = dict()
#         recipe['id'] = object.token
#         recipe['doctorName'] = object.doctor.user.last_name + ' ' + object.doctor.user.first_name
#         recipe['patientName'] = object.patient_initials
#         # recipe['patient_email'] = object.patient_email
#         recipe['date'] = object.date.strftime('%d.%m.%Y')
#         return recipe


class RecipeShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'doctorName', 'patientName', 'patient_email', 'date')
    id = CharField(source='token')
    doctorName = CharField(source='get_doctor_initials')
    patientName = CharField(source='patient_initials')
    date = CharField(source='get_date_str')
    

class MedicineRequestSerializer(JsonSerializer):
    @staticmethod
    def get_json(object: MedicineRequest):
        result = dict()
        result['is_accepted'] = object.medicine_count > 0
        result['medicine_name'] = object.medicine_dosage.medicine.medicine_name
        result['medicine_frequency'] = object.medicine_dosage.frequency
        result['medicine_dosage'] = object.medicine_dosage.dosage
        result['medicine_period'] = object.medicine_dosage.period
        return result


class RecipeSerializerFull(JsonSerializer):
    @staticmethod
    def get_json(object: Recipe):
        recipe = dict()
        recipe['id'] = object.id
        recipe['doctor_initials'] = object.doctor.user.last_name + ' ' + object.doctor.user.first_name
        recipe['doctor_email'] = object.doctor.user.email
        recipe['patient_initials'] = object.patient_initials
        recipe['patient_email'] = object.patient_email
        recipe['date'] = object.date.strftime('%Y-%m-%d %H:%M')
        recipe['day_duration'] = object.day_duration
        recipe['patient_age'] = object.patient_age
        recipe['medicine_card_number'] = object.medicine_card_number
        recipe['medicine_policy_number'] = object.medicine_policy_number
        medicineRequests = object.medicinerequest_set.all()
        requests = [MedicineRequestSerializer.get_json(i) for i in medicineRequests]
        recipe['requests'] = requests
        return recipe


# class UserSerializer(JsonSerializer):
#     @staticmethod
#     def get_json(object):
#         role = get_role(object)
#         return {
#           'id': object.id,
#           'email': object.email,
#           'last_name': object.last_name,
#           'first_name': object.first_name,
#           'phone_number': object.phone_number,
#           'role': role,
#         }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'last_name', 'first_name', 'phone_number', 'role')
        
    def save(self, **kwargs):
        super().save(**kwargs)
    

