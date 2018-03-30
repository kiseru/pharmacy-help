from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.forms import EmailField, CharField

from recipes.models import User


class MyUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'phone_number')
        field_classes = {'email': EmailField, 'phone_number': CharField}

