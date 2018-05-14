from django.forms import ModelForm, PasswordInput, CharField
from django.shortcuts import get_object_or_404

from recipes.models import User, Medicine, MedicineType, MedicineName, MedicinesPharmacies, Apothecary


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['email', 'phone_number', 'last_name', 'first_name']
    password = CharField(widget=PasswordInput, required=False)
    repeat_password = CharField(widget=PasswordInput, required=False)

    def is_valid(self):
        if super().is_valid():
            if self.data['password'] or self.data['repeat_password']:
                if self.data['password'] != self.data['repeat_password']:
                    self.add_error('repeat_password', 'Passwords should be same')
                    return False
                try:
                    self.instance.set_password(self.data['password'])
                except:
                    self.add_error('password', 'Password is incorrect')
                    return False
        return not self.errors


class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']
    password = CharField(widget=PasswordInput())

#Формы для добавления лекарств
class MedicineForm(ModelForm):
    class Meta:
        model = Medicine
        fields = ()

    def save(self, request, m1, m2, m3, *args, **kwargs):
        instance = self.instance
        instance.medicine_name = m2
        instance.medicine_type = m1
        instance.save()
        MedicinesPharmacies(pharmacy=get_object_or_404(Apothecary,**{'user':request.user}).pharmacy,
                            medicine=instance, count=m3.data['count'], price=m3.data['price']).save()
        return super()


class MedicineTypeForm(ModelForm):
    class Meta:
        model = MedicineType
        fields = ('type_name',)

class MedicineNamesForm(ModelForm):
    class Meta:
        model = MedicineName
        fields = ('medicine_name', 'medicine_description', 'medicine_level',)

class MedicinePharmacyForm(ModelForm):
    class Meta:
        model = MedicinesPharmacies
        fields = ('count','price')
