from rest_framework.fields import CharField

from recipes.models import Recipe, MedicineRequest, User, Medicine, MedicineType, MedicineName
from rest_framework import serializers


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
        fields = ('id', 'email', 'last_name', 'first_name', 'phone_number', 'role')
        
    def save(self, **kwargs):
        super().save(**kwargs)
        

class MedicineTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicineType
        fields = ('id', 'type_name')


class MedicineNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicineName
        fields = ('id', 'medicine_name', 'medicine_types')
    medicine_types = MedicineTypeSerializer(many=True)

