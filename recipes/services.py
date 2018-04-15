import re

from django.contrib.auth.hashers import MD5PasswordHasher
from django.db import transaction
from django.db.models import Q
from django.utils import timezone

from recipes.models import Recipe, MedicineDosage, MedicineRequest, MedicineName


def get_recipes(query: str=None):
    if query:
        query = query.replace(' ', '')
        # q1 = Recipe.objects.filter(medicine_policy_number__contains=query)
        # q2 = Recipe.objects.filter(medicine_card_number__contains=query)
        # q3 = Recipe.objects.filter(patient_email__contains=query)
        q4 = Recipe.objects.filter(token__contains=query)
        # result = q1 | q2 | q3 | q4
        result = q4
        return result
    return Recipe.objects.all()


@transaction.atomic
def create_recipe(data: dict, user):
        flag = contains_highlevel_medicines(data['medicines'])
        if flag:
            if not ('medicine_policy_number' in data
                    and 'medicine_card_number' in data
                    and data['medicine_policy_number']
                    and data['medicine_card_number']):
                raise Exception('More data is required')

        doctor = user.doctor_set.all()[0]
        recipe = Recipe(
            patient_age=data['patient_age'],
            patient_email=data['patient_email'],
            patient_initials=data['patient_initials'],
            medicine_card_number=data['medicine_card_number'],
            medicine_policy_number=data['medicine_policy_number'],
            day_duration=15 if flag else data['day_duration'],
            token=get_hash(data['patient_email'], doctor.id, timezone.now()),
            doctor=doctor
        )
        recipe.full_clean()
        recipe.save()
        for i in data['medicines']:
            medicine = MedicineName.objects.get(pk=i['medicine_id'])
            medicine_dosage = MedicineDosage(
                medicine=medicine,
                frequency=i['frequency'],
                period=i['period'],
                dosage=i['dosage'],
            )
            medicine_dosage.full_clean()
            medicine_dosage.save()
            # objects_for_saving.append(medicine_dosage)
            request = MedicineRequest(
                medicine_dosage=medicine_dosage,
                recipe=recipe,
            )
            request.save()


def contains_highlevel_medicines(medicinelist: list):
    for i in medicinelist:
        id = i['medicine_id']
        medicine = MedicineName.objects.get(pk=id)
        if medicine.medicine_level:
            return True
    return False


def get_hash(*args):
    string = ''.join(str(i) for i in args)
    return MD5PasswordHasher().encode(string, '1')[6:]
