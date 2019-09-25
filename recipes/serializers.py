import re

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField, IntegerField

from recipes import models
from recipes.models import Recipe, MedicineRequest, User, Medicine, MedicineType, MedicineName, Pharmacy


def serialize_user(user, errors: list):
    result = UserSerializer(instance=user)
    result.data['error'] = None if not errors else ''.join(
        [''.join([j[1][0]['message'] for j in i.items()]) for i in errors])
    return result.data


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
