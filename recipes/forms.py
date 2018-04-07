from django.forms import ModelForm, PasswordInput, CharField

from recipes.models import User


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