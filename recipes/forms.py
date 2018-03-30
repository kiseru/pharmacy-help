from django.forms import ModelForm, PasswordInput, CharField

from recipes.models import User


class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']
    password = CharField(widget=PasswordInput())