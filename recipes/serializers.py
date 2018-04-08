from recipes.auth import *
from recipes.models import Recipe, MedicineRequest


class JsonSerializer:
    def get_json(self, object):
        return object.__str__()

def serialize_user(user, errors: list):
    role = get_role(user)
    return {
            'id': user.id,
            'email': user.email,
            'last_name': user.last_name,
            'first_name': user.first_name,
            'phone_number': user.phone_number,
            'role': role,
            'error':  None if not errors else ''.join([''.join([j[1][0]['message'] for j in i.items()]) for i in errors]),
    }

class RecipeSerializerShort(JsonSerializer):
    def get_json(self, object: Recipe):
        recipe = dict()
        recipe['id'] = object.id
        recipe['doctor_initials'] = object.doctor.user.last_name + ' ' + object.doctor.user.first_name
        recipe['patient_initials'] = object.patient_initials
        recipe['patient_email'] = object.patient_email
        recipe['date'] = object.date.strftime('%Y-%m-%d %H:%M')
        return recipe


class MedicineRequestSerializer(JsonSerializer):
    def get_json(self, object: MedicineRequest):
        result = dict()
        result['is_accepted'] = object.medicine_count > 0
        result['medicine_name'] = object.medicine_dosage.medicine.medicine_name
        result['medicine_frequency'] = object.medicine_dosage.frequency
        result['medicine_dosage'] = object.medicine_dosage.dosage
        result['medicine_period'] = object.medicine_dosage.period
        return result


class RecipeSerializerFull(JsonSerializer):
    medicineRequestSerializer = MedicineRequestSerializer()

    def get_json(self, object: Recipe):
        recipe = dict()
        recipe['id'] = object.id
        recipe['doctor_initials'] = object.doctor.user.last_name + ' ' + object.doctor.user.first_name
        recipe['doctor_email'] = object.doctor.user.email
        recipe['patient_initials'] = object.patient_initials
        recipe['patient_email'] = object.patient_email
        recipe['date'] = object.date.strftime('%Y-%m-%d %H:%M')
        recipe['day_duration'] = object.day_duration
        recipe['patient_age'] = object.patient_age
        recipe['medicine_card_number'] = object.medicine_card_number
        recipe['medicine_policy_number'] = object.medicine_policy_number
        medicineRequests = object.medicinerequest_set.all()
        requests = [self.medicineRequestSerializer.get_json(i) for i in medicineRequests]
        recipe['requests'] = requests
        return recipe
