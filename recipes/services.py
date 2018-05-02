import re

from django.contrib.auth.hashers import MD5PasswordHasher
from django.db import transaction
from django.db.models import Q
from django.utils import timezone

from recipes.models import Recipe, MedicineDosage, MedicineRequest, MedicineName, MedicinesPharmacies


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


@transaction.atomic()
def serve_recipe(medicines, recipe, apothecary):
    for m in medicines:
        medicine_requests = MedicineRequest.objects.filter(
              recipe=recipe,
              medicine_dosage__medicine__pk=m['medicine_name_id'])
        if medicine_requests.count():
            medicine_request = medicine_requests[0]
            if not medicine_request.request_confirmation_time:
                medicine_request.apothecary = apothecary
                medicine_request.medicine_count = m['medicine_count']
                medicine_request.request_confirmation_time = timezone.now()
                medicine_request.given_medicine_id = m['medicine_id']
                pharmacy = apothecary.pharmacy
                goods = pharmacy.medicinespharmacies_set.filter(medicine_id=m['medicine_id'])
                if goods.count():
                    good = goods.all()[0]
                    if good.count >= m['medicine_count']:
                        good.count -= m['medicine_count']
                        MedicinesPharmacies.save(good)
                    else:
                        raise Exception('invalid_data')
                else:
                    raise Exception('invalid_data')
                MedicineRequest.save(medicine_request)
            else:
                raise Exception('invalid_data')
        else:
            raise Exception('invalid_data')


