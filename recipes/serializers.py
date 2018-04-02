def serialize_user(user):
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
        'role':role,
    }