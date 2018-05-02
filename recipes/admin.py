from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin
from django.forms import ModelForm
from django.utils.translation import gettext, gettext_lazy as _

# Register your models here.
from recipes.admin_forms import MyUserChangeForm, MyUserCreationForm, PharmacyForm
from recipes.models import User, Medicine, MedicineName, Doctor, Apothecary, Pharmacy, Recipe, MedicineType, \
  MedicineRequest, MedicineRequestStatus, MedicineDosage, MedicinesPharmacies
from recipes.services import get_coordinates


class MyUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'phone_number', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                        )}),

    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone_number', 'password1', 'password2'),
        }),
    )
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    list_display = ( 'email', 'phone_number', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ( 'first_name', 'phone_number', 'last_name', 'email')
    ordering = ('last_name',)
    filter_horizontal = []


class PharmacyAdminForm(ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        if request.user.is_superuser:
            kwargs['form'] = PharmacyForm
        return super().get_form(request, obj, **kwargs)


admin.site.register(User, MyUserAdmin)
admin.site.register(Medicine)
admin.site.register(MedicineName)
admin.site.register(Doctor)
admin.site.register(Apothecary)
admin.site.register(Pharmacy, PharmacyAdminForm)
admin.site.register(Recipe)
admin.site.register(MedicineType)
admin.site.register(MedicineRequest)
admin.site.register(MedicineRequestStatus)
admin.site.register(MedicineDosage)
admin.site.register(MedicinesPharmacies)
