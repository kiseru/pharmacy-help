import json
import re
import traceback
import math

import requests
from django.contrib.auth.hashers import MD5PasswordHasher
from django.db import transaction
from django.db.models import Q
from django.utils import timezone

from recipes.models import Recipe, MedicineDosage, MedicineRequest, MedicineName, MedicinesPharmacies, Pharmacy, \
  Medicine


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


def get_coordinates(address: str):
    response = requests.get('https://geocode-maps.yandex.ru/1.x/?format=json&geocode={}'.format(address))
    data = json.loads(response.content.decode(response.encoding))
    try:
        coordinates_str = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
        x, y = map(lambda s: float(s), coordinates_str.split())
        return y, x
    except:
        pass


def find_pharmacies(city_name, medicine_ids, coordinates=None):
    result = []
    pharmacies = Pharmacy.objects.filter(city__name=city_name)
    medicines = [Medicine.objects.get(id=m) for m in medicine_ids]
    pharmacies_goods = dict()
    for p in pharmacies:
        pharmacies_goods[p] = [[], 0]
        for m in medicines:
            if MedicinesPharmacies.objects.filter(pharmacy=p, medicine=m).count():
                pharmacies_goods[p][0].append(m.id)
                pharmacies_goods[p][1] = get_distance(*coordinates, p.latitude, p.longitude)
    found_medicines = 0
    required_medicines = len(medicines)
    pharmacies_goods_list = [(k, v) for (k, v) in pharmacies_goods.items()]
    while found_medicines < required_medicines:
        pharmacies_goods_list = sorted(pharmacies_goods_list, key=lambda x: (-len(x[1][0]), x[1][1]))
        print(pharmacies_goods_list)
        if len(pharmacies_goods_list[0][1][0]) == 0:
            break
        result.append(pharmacies_goods_list[0][0])
        
        for m in pharmacies_goods_list[0][1][0]:
            print('remove ', m)
            found_medicines += 1
            for k, v in pharmacies_goods_list:
                print('now ', k, v)
                if m in v[0]:
                    print('remove', m, 'from', k)
                    v[0].remove(m)
        
        pharmacies_goods_list = pharmacies_goods_list[1:]
        
    return result
    
    
def get_distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
