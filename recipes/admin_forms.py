from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.forms import EmailField, CharField, ModelForm

from recipes.models import User
from recipes.services import get_coordinates


class MyUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'phone_number')
        field_classes = {'email': EmailField, 'phone_number': CharField}


class PharmacyForm(ModelForm):
    def is_valid(self):
        if super().is_valid():
            try:
                x, y = get_coordinates(self.data['pharmacy_address'])
                self.instance.latitude = x
                self.instance.longitude = y
                return True
            except:
                self.add_error('pharmacy_address', "Address isn't valid. Can't determine coordinates.")
                return False
        return not self.errors
