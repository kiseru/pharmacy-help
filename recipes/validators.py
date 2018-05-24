from django.core.exceptions import ValidationError


def validate_pos_value(value):
    if value <= 0:
        raise ValidationError('Please enter a positive number, %s is invalid value' % value)
