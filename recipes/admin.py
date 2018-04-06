from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext, gettext_lazy as _

# Register your models here.
from recipes.admin_forms import MyUserChangeForm, MyUserCreationForm
from recipes.models import User, Medicine, MedicineName, Doctor, Apothecary, Pharmacy


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



admin.site.register(User, MyUserAdmin)
admin.site.register(Medicine)
admin.site.register(MedicineName)
admin.site.register(Doctor)
admin.site.register(Apothecary)
admin.site.register(Pharmacy)