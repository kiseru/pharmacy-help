def get_role(user):
    if user.doctor:
        role = 'doctor'
    elif user.apothecary_set.count():
        role = 'apothecary'
    else:
        raise Exception('No such role')
    return role

