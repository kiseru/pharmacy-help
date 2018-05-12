import re

from django.db.models import Q

from recipes.models import Recipe


def get_recipes(query: str=None):
    if query:
        query = query.replace(' ', '')
        # q1 = Recipe.objects.filter(medicine_policy_number__contains=query)
        # q2 = Recipe.objects.filter(medicine_card_number__contains=query)
        # q3 = Recipe.objects.filter(patient_email__contains=query)
        q4 = Recipe.objects.filter(token__contains=query)
        # result = q1 | q2 | q3 | q4
        result = q4
        return result
    return Recipe.objects.all()
