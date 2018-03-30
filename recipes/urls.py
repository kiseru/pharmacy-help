from django.conf.urls import url

from recipes.views import profile

urlpatterns = [
    url(r'profile$', profile, name='profile')
]