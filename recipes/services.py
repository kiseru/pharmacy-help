import json
import math

import requests

from recipes.models import Good, Pharmacy, Medicine
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
