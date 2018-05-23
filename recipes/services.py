import json
import re
import traceback
import math

import requests
from django.contrib.auth.hashers import MD5PasswordHasher
from django.core.mail import send_mail
from django.db import transaction
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from pharmacyhelp import settings
from recipes.auth import get_role
from recipes.exceptions import AlreadyExistsException
from recipes.models import Recipe, MedicineDosage, MedicineRequest, MedicineName, MedicinesPharmacies, Pharmacy, \
  Medicine, User, Apothecary, Doctor, MedicineType
from recipes.serializers import PharmacySerializer, MedicineSerializer


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
def create_recipe(recipe, data: dict, request):
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
            
            medicine_request = MedicineRequest(
                medicine_dosage=medicine_dosage,
                recipe=recipe,
            )
            medicine_request.save()
        try:
            send_email_recipe(request, recipe)
        except:
            traceback.print_exc()
            raise ValidationError()


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
def serve_recipe(requests, recipe, apothecary):
    for r in requests:
        request = MedicineRequest.objects.get(pk=r['id'])
        if request.recipe.id != recipe.id:
            raise Exception('invalid_data')
        request.apothecary = apothecary
        request.request_confirmation_time = timezone.now()
        pharmacy = apothecary.pharmacy
        goods = pharmacy.medicinespharmacies_set.filter(id=r['given_medicine'])
        if goods.count():
            good = goods.first()
            # проверяем, действительно ли выдается препарат, соответствующий данному medicine_request
            if request.medicine_dosage.medicine.id != good.medicine.medicine_name.id:
                raise ValidationError()
            if good.count >= r['medicine_count']:
                good.count -= r['medicine_count']
                MedicinesPharmacies.save(good)
                request.medicine_count = r['medicine_count']
                request.given_medicine_id = good.medicine.id
                MedicineRequest.save(request)
            else:
                raise ValidationError()
        else:
            raise ValidationError()
        MedicineRequest.save(request)


def get_coordinates(address: str):
    response = requests.get('https://geocode-maps.yandex.ru/1.x/?format=json&geocode={}'.format(address))
    data = json.loads(response.content.decode(response.encoding))
    try:
        coordinates_str = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
        x, y = map(lambda s: float(s), coordinates_str.split())
        return y, x
    except:
        pass


def get_pharmacies_and_medicines(data):
    city = data['city_name']
    print(city)
    medicines = data['medicines']
    print(medicines)
    coordinates = data['coordinates'] if 'coordinates' in data else None
    result = find_pharmacies(city, medicines, coordinates)
    return [{'pharmacy':PharmacySerializer(k).data, 'medicines': [MedicineSerializer(i).data for i in v]} for k, v in result.items()]


def find_pharmacies(city_name, medicine_ids, coordinates=None):
    result = dict()
    if not coordinates:
        coordinates = get_coordinates(city_name)
    pharmacies = Pharmacy.objects.filter(city__name=city_name)
    medicines = [Medicine.objects.get(id=m) for m in medicine_ids]
    pharmacies_goods = dict()
    for p in pharmacies:
        pharmacies_goods[p] = [[], 0]
        for m in medicines:
            if MedicinesPharmacies.objects.filter(pharmacy=p, medicine=m).count():
                pharmacies_goods[p][0].append(m)
                pharmacies_goods[p][1] = get_distance(*coordinates, p.latitude, p.longitude)
    found_medicines = 0
    required_medicines = len(medicines)
    pharmacies_goods_list = pharmacies_goods.items()
    while found_medicines < required_medicines:
        pharmacies_goods_list = sorted(pharmacies_goods_list, key=lambda x: (-len(x[1][0]), x[1][1]))
        if len(pharmacies_goods_list[0][1][0]) == 0:
            break
        
        pharmacy = pharmacies_goods_list[0]
        pharmacies_goods_list = pharmacies_goods_list[1:]

        result[pharmacy[0]] = []
        
        for m in pharmacy[1][0]:
            result[pharmacy[0]].append(m)
            found_medicines += 1
            for k, v in pharmacies_goods_list:
                if m in v[0]:
                    v[0].remove(m)
        
    return result
    
    
def get_distance(x1, y1, x2, y2):
    lon1, lat1, lon2, lat2 = map(math.radians, [x1, y1, x2, y2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371  # radius of Earth in kilometers
    return c * r


@transaction.atomic()
def add_worker(user_serializer, admin):
    if not user_serializer.is_valid():
        if 'email' in user_serializer.errors or 'phone_number' in user_serializer.errors:
            raise AlreadyExistsException(User)
        else:
            print(user_serializer.errors)
            raise ValidationError()
    user = User.objects.create_user(**user_serializer.validated_data)
    if get_role(admin) == 'apothecary':
        pharmacy = admin.apothecary_set.all()[0].pharmacy
        apothecary = Apothecary(pharmacy=pharmacy, user=user)
        Apothecary.save(apothecary)
    else:
        hospital = admin.doctor_set.all()[0].hospital
        doctor = Doctor(user=user, hospital=hospital)
        Doctor.save(doctor)
    return user


def update_user(serializer, user):
    if serializer.initial_data.get('email', '') and serializer.initial_data['email'] != user.email:
        if User.objects.filter(email=serializer.initial_data['email']).count():
            raise AlreadyExistsException(User)
        user.email = serializer.data['email']
    if serializer.initial_data.get('phone_number', '') and serializer.initial_data['phone_number'] != user.phone_number:
        if User.objects.filter(phone_number=serializer.initial_data['phone_number']).count():
            raise AlreadyExistsException(User)
        user.phone_number = serializer.data['phone_number']
    if serializer.initial_data.get('password', ''):
        user.set_password(serializer.initial_data['password'])
    if serializer.is_valid() or ('first_name' not in serializer.errors and 'last_name' not in serializer.errors):
        user.first_name = serializer.data['first_name']
        user.last_name = serializer.data['last_name']
        User.save(user)
    else:
        raise ValidationError()


def get_workers(user, query=None):
    if get_role(user) == 'apothecary':
        pharmacy = user.apothecary_set.all()[0].pharmacy
        result = User.objects.filter(apothecary__pharmacy=pharmacy)
    else:
        hospital = user.doctor_set.all()[0].hospital
        result = User.objects.filter(doctor__hospital=hospital)
    if query:
        q1 = result.filter(email__icontains=query)
        q2 = result.filter(phone_number__icontains=query)
        q3 = result.filter(first_name__icontains=query)
        q4 = result.filter(last_name__icontains=query)
        result = q1 | q2 | q3 | q4
    return result


def send_email_recipe(request, recipe):
    if settings.SEND_EMAIL:
        text = 'Здравствуйте, {}!\nВам выписан рецепт. Посмотреть рецепт можно по ссылке: {}'.format(
            recipe.patient_initials, request.build_absolute_uri(reverse('show_recipe', args=(recipe.token, )))
        )
        send_mail('Уведомление о рецепте', text, settings.EMAIL_HOST_USER, [recipe.patient_email])


def get_or_create_medicine_name(name, level, description):
    medicines = MedicineName.objects.filter(
        medicine_name__iexact=name,
        medicine_level=level,
        medicine_description__iexact=description
    )
    if medicines.count():
        return medicines.all()[0]
    else:
        medicine_name = MedicineName(medicine_name=name, medicine_description=description, medicine_level=level)
        MedicineName.save(medicine_name)
        return medicine_name


def get_or_create_medicine_type(type):
    medicines = MedicineType.objects.filter(type_name__iexact=type)
    if medicines.count():
        return medicines.all()[0]
    else:
        medicine_type = MedicineType(type_name=type)
        MedicineType.save(medicine_type)
        return medicine_type


def get_or_create_medicine(medicine_name, medicine_type):
    medicines = Medicine.objects.filter(medicine_name=medicine_name, medicine_type=medicine_type)
    if medicines.count():
        return medicines.all()[0]
    else:
        medicine = Medicine(medicine_type=medicine_type, medicine_name=medicine_name)
        Medicine.save(medicine)
        return medicine


@transaction.atomic()
def add_medicine(data, user):
    try:
        medicine_name = get_or_create_medicine_name(data['name'], data['level'], data.get('description', '-'))
        medicine_type = get_or_create_medicine_type(data['type'])
        medicine = get_or_create_medicine(medicine_name=medicine_name, medicine_type=medicine_type)
        pharmacy = user.apothecary_set.all()[0].pharmacy
        goods = MedicinesPharmacies.objects.filter(medicine=medicine, pharmacy=pharmacy)
        if goods.count():
            raise AlreadyExistsException(MedicinesPharmacies)
        good = MedicinesPharmacies(
            medicine=medicine,
            pharmacy=pharmacy,
            count=data['count'],
            price=data['price'],
        )
        MedicinesPharmacies.save(good)
        return good
    except KeyError:
        raise ValidationError()
    
    
@transaction.atomic()
def update_medicine(good, data):
    try:
        good.count = data['count']
        good.price = data['price']
        MedicinesPharmacies.save(good)
    except KeyError:
        raise ValidationError()
