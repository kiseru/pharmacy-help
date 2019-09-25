from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin

from recipes import models
from recipes.admin_forms import MyUserChangeForm, MyUserCreationForm


@admin.register(models.Apothecary)
class ApothecaryAdmin(admin.ModelAdmin):
    list_display = ('user', 'pharmacy')
    search_fields = ('pharmacy__pharmacy_name',
                     'user__first_name',
                     'user__last_name')


@admin.register(models.City)
class CityAdmin(admin.ModelAdmin):
    search_fields = ('name',)


@admin.register(models.Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'hospital')
    search_fields = ('hospital__hospital_name',
                     'user__first_name',
                     'user__last_name',
                     'user__email')


@admin.register(models.Good)
class GoodAdmin(admin.ModelAdmin):
    list_display = ('medicine', 'pharmacy', 'count', 'price')


@admin.register(models.Hospital)
class HospitalAdmin(admin.ModelAdmin):
    autocomplete_fields = ('city',)
    list_display = ('hospital_name', 'city')
    search_fields = ('hospital_name', 'city__name')


@admin.register(models.MedicineName)
class MedicineNameAdmin(admin.ModelAdmin):
    search_fields = ('medicine_name',)


@admin.register(models.User)
class MyUserAdmin(UserAdmin):
    fieldsets = (
        ('Персональная информация',
         {'fields': ('last_name', 'first_name', 'email', 'phone_number', 'password', 'is_admin')}),
        ('Статусы', {'fields': ('is_active', 'is_staff', 'is_superuser')}),

    )
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    list_display = ('first_name', 'last_name', 'email', 'phone_number',
                    'is_admin')
    list_filter = ('is_admin',)
    search_fields = ('first_name', 'phone_number', 'last_name', 'email')
    ordering = ('last_name',)
    filter_horizontal = []


@admin.register(models.Pharmacy)
class PharmacyAdmin(ModelAdmin):
    list_display = ('pharmacy_name', 'city', 'pharmacy_address')
    search_fields = ('pharmacy_name', 'city__name', 'pharmacy_address')


@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    autocomplete_fields = ('doctor',)
    list_display = ('patient_email', 'patient_initials', 'token', 'date')
    ordering = ('-date',)
    readonly_fields = ('token',)
    search_fields = ('patient_email', 'patient_initials', 'token', 'date')


admin.site.register(models.Medicine)
admin.site.register(models.MedicineType)
admin.site.register(models.MedicineRequest)
admin.site.register(models.MedicineRequestStatus)
admin.site.register(models.MedicineDosage)
