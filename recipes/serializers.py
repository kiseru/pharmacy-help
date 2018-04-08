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
