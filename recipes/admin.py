from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from recipes import models
from recipes.admin_forms import MyUserChangeForm, MyUserCreationForm, \
    PharmacyForm
from recipes.models import User, Medicine, MedicineName, Doctor, Apothecary, \
    Pharmacy, MedicineType, MedicineRequest, MedicineRequestStatus, \
    MedicineDosage, City, Hospital


@admin.register(models.Good)
class GoodAdmin(admin.ModelAdmin):
    list_display = ('medicine', 'pharmacy', 'count', 'price')


@admin.register(User)
class MyUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'phone_number', 'password', 'is_admin')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       )}),

    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone_number', 'password1', 'password2',
                       'first_name', 'last_name'),
        }),
    )
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    list_display = ('email', 'phone_number', 'first_name', 'last_name',
                    'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('first_name', 'phone_number', 'last_name', 'email')
    ordering = ('last_name',)
    filter_horizontal = []


@admin.register(Pharmacy)
class PharmacyAdmin(ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        if request.user.is_superuser:
            kwargs['form'] = PharmacyForm
        return super().get_form(request, obj, **kwargs)


@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    readonly_fields = ('token',)


admin.site.register(Medicine)
admin.site.register(MedicineName)
admin.site.register(Doctor)
admin.site.register(Apothecary)
admin.site.register(MedicineType)
admin.site.register(MedicineRequest)
admin.site.register(MedicineRequestStatus)
admin.site.register(MedicineDosage)
admin.site.register(City)
admin.site.register(Hospital)
