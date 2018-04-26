import re

from django.contrib.auth.hashers import MD5PasswordHasher
from django.db import transaction
from django.db.models import Q
from django.utils import timezone

from recipes.models import Recipe, MedicineDosage, MedicineRequest, MedicineName


def get_recipes(query: str=None, recipes=Recipe.objects):
    if query:
        query = query.replace(' ', '')
        # q1 = recipes.filter(medicine_policy_number__contains=query)
        # q2 = recipes.filter(medicine_card_number__contains=query)
        q3 = recipes.filter(patient_email__contains=query)
        q4 = recipes.filter(token__contains=query)
        result = q3 | q4
        # result = q4
        return result
    return Recipe.objects.all()


def get_recipes_of_doctor(doctor, query=''):
    return get_recipes(query, doctor.recipe_set)
    

@transaction.atomic
def create_recipe(recipe, data: dict):
        flag = contains_highlevel_medicines(data['medicines'])
        if flag:
            if not (recipe.medicine_policy_number
                    and recipe.medicine_card_number):
                raise Exception('more_required')
            if len(data['medicines']) > 1:
                raise Exception('too_much_medicines')

        recipe.token=get_hash(recipe.patient_email, recipe.doctor.id, timezone.now())
        recipe.full_clean()
        recipe.save()
        for i in data['medicines']:
            medicine = MedicineName.objects.get(pk=i['medicine_id'])
            medicine_dosage = MedicineDosage(**i, medicine=medicine)
            medicine_dosage.full_clean()
            medicine_dosage.save()
            
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
