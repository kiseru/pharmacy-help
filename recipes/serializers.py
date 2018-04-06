def serialize_user(user, errors: list):
    if user.doctor_set.count():
        role = 'doctor'
    elif user.apothecary_set.count():
        role = 'apothecary'
    else:
        role = None
    return {
            'id': user.id,
            'email': user.email,
            'last_name': user.last_name,
            'first_name': user.first_name,
            'phone_number': user.phone_number,
            'role': role,
            'error':  None if not errors else ''.join([''.join([j[1][0]['message'] for j in i.items()]) for i in errors]),
    }