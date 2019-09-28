import re

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField, IntegerField

from recipes import models
from recipes.models import Recipe, MedicineRequest, User, Medicine, Pharmacy


class MedicineRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicineRequest
        fields = ['id', 'medicine_name_id', 'is_accepted', 'medicine_name', 'medicine_frequency', 'dosage',
                  'medicine_period', 'given_medicine', 'medicine_count']


class MedicineRequestSerializerForUpdate(serializers.ModelSerializer):
    class Meta:
        model = MedicineRequest
        fields = ['id', 'given_medicine', 'medicine_count']

    id = IntegerField(required=True)
    extra_kwargs = {
        'given_medicine': {'write_only': True},
        'medicine_count': {'write_only': True},
    }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'last_name', 'first_name', 'phone_number', 'role', 'is_admin', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.City
        fields = '__all__'


class HospitalSerializer(serializers.ModelSerializer):
    city = CitySerializer()

    class Meta:
        model = models.Hospital
        fields = '__all__'


class DoctorSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    hospital = HospitalSerializer()

    class Meta:
        model = models.Doctor
        fields = '__all__'


class RecipeSerializer(serializers.ModelSerializer):
    requests = MedicineRequestSerializer(required=False, many=True,
                                         read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'patient_initials', 'patient_email', 'date',
                  'day_duration', 'patient_age', 'medicine_card_number',
                  'medicine_policy_number', 'requests', 'comment', 'token')
        read_only_fields = ('token',)


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


class MedicineSerializer(serializers.ModelSerializer):
    medicine_name = CharField(source='name')
    medicine_type = CharField(source='type')

    class Meta:
        model = Medicine
        fields = ('id', 'medicine_name', 'medicine_type')


class GoodSerializer(serializers.ModelSerializer):
    medicine = serializers.PrimaryKeyRelatedField(queryset=models.Medicine.objects.all())

    class Meta:
        model = models.Good
        fields = ('count', 'price', 'name', 'type', 'id', 'level', 'medicine')


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=20)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class ApothecarySerializer(serializers.ModelSerializer):
    pharmacy = PharmacySerializer(read_only=True)
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(apothecary=None, doctor=None),
                                                 source='user')

    class Meta:
        model = models.Apothecary
        fields = ('pharmacy', 'user', 'user_id')
        read_only_fields = ('pharmacy', 'user')
