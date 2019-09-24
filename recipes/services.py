import json
import math

import requests
from django.db import transaction
from rest_framework.exceptions import ValidationError

from recipes.auth import get_role
from recipes.exceptions import AlreadyExistsException
from recipes.models import Good, Pharmacy, \
    Medicine, User, Apothecary, Doctor
from recipes.serializers import PharmacySerializer, MedicineSerializer


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
            if Good.objects.filter(pharmacy=p, medicine=m).count():
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


def delete_worker(user):
    User.delete(user)


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
